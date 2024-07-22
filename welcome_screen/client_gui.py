import subprocess
import socket
import threading
import tkinter as tk
from tkinter import messagebox
import atexit
import json
import time

def get_server_address():
    try:
        with open('../config/config.json', 'r') as f:
            config = json.load(f)
            return config.get('server_address', '')
    except FileNotFoundError:
        return ''

class UDPClient:
    def __init__(self, server_ip=get_server_address(), server_port=5556):
        self.server_address = (server_ip, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(10)  # Set a 10-second timeout for socket operations
        self.client_id = None
        self.running = True # for recieve thread
        self.running_monitor = False # for monitor thread
        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.user_list = []
        self.update_callback = None
        self.client_process = None
        self.check_client_thread = None

    def send(self, message):
        self.sock.sendto(message.encode(), self.server_address)

    def receive(self):
        while self.running:
            try:
                response, _ = self.sock.recvfrom(4096)
                decoded_response = response.decode()
                if decoded_response.startswith("ID:"):
                    self.client_id = decoded_response.split(":")[1]
                    print(f"Assigned ID: {self.client_id}")
                    if self.update_callback:
                        self.update_callback(client_id_updated=True)
                elif decoded_response.startswith("USERLIST:"):
                    self.user_list = [user for user in decoded_response.split(":")[1].split(",") if user and user != self.client_id]
                    print(f"Updated user list: {self.user_list}")
                    if self.update_callback:
                        self.update_callback(client_id_updated=False)
                elif decoded_response.startswith("REQUEST:"):
                    requester_id = decoded_response.split(":")[1]
                    if self.update_callback:
                        self.update_callback(client_id_updated=False, request=requester_id)
                elif decoded_response.startswith("ACCEPT:"):
                    partner_id = decoded_response.split(":")[1]
                    print(f"Request accepted by {partner_id}")
                    if self.update_callback:
                        self.update_callback(client_id_updated=False, accepted=partner_id)
                elif decoded_response == "START_CLIENT":
                    if not self.client_process or self.client_process.poll() is not None:
                        self.start_client_process()
                elif decoded_response == "SHUTDOWN":
                    self.terminate_client_process()
                else:
                    print(f"Server response: {decoded_response}")
            except socket.timeout:
                print("Socket timeout. Retrying...")
                continue
            except Exception as e:
                print(f"Error: {e}")
                self.disconnect()
                break

    def connect(self):
        try:
            print(self.server_address)
            self.send("CONNECT")
            self.sock.recvfrom(4096)  # Blocking call to wait for server response
            self.receive_thread.start()
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
        return True

    def request_user_list(self):
        self.send("GET")

    def disconnect(self):
        if self.client_id is not None:
            self.send(f"DISCONNECT:{self.client_id}")
            print("Sending disconnect to server")
        self.running = False

        # Only join the thread if it's alive
        if self.receive_thread.is_alive():
            try:
                self.receive_thread.join()
            except RuntimeError:
                print("Attempted to join the current thread. Skipping join.")

        self.sock.close()
        print("Disconnected from server.")

        # Shutdown subprocess if running
        self.terminate_client_process()

    def send_request(self, target_id):
        if self.client_id:
            self.send(f"REQUEST:{self.client_id}:{target_id}")

    def accept_request(self, requester_id):
        if self.client_id:
            self.send(f"ACCEPT:{self.client_id}:{requester_id}")

    def start_client_process(self):
        try:
            self.client_process = subprocess.Popen(['python3', '../multi_comp/client.py'])
            print("Started client.py")
            

            # Start a separate thread to check if the subprocess has terminated
            if self.check_client_thread and self.check_client_thread.is_alive():
                self.check_client_thread.join()

            self.running_monitor = True
            self.check_client_thread = threading.Thread(target=self.monitor_client_process, daemon=True)
            self.check_client_thread.start()
        except Exception as e:
            print(f"Error starting client.py: {e}")

    def monitor_client_process(self):
        while self.running_monitor:
            if self.client_process.poll() is not None:
                print("client.py subprocess has ended. Sending shutdown message to server.")
                self.send("SHUTDOWN")
                # Optionally restart the process if needed
                # self.start_client_process()
                break
            time.sleep(1)  # Check every second

    def terminate_client_process(self):
        # Signal the monitoring thread to stop, if it is running
        if self.check_client_thread and self.check_client_thread.is_alive():
            self.running_monitor = False  # This will signal the monitoring thread to stop
            self.check_client_thread.join()  # Wait for the thread to finish
            print("Monitoring thread has been stopped.")

        if self.client_process and self.client_process.poll() is None:
            self.client_process.terminate()
            self.client_process.wait()  # Ensure it has terminated
            print("Terminated client.py subprocess.")

        # If needed, restart the receive loop
        if not self.receive_thread.is_alive():
            self.receive_thread = threading.Thread(target=self.receive, daemon=True)
            self.receive_thread.start()

class Application(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.title("Tkinter User Lobby")
        self.geometry("400x300")
        
        self.client = client
        
        self.button = tk.Button(self, text="Connect to the server", command=self.on_button_click, width=20, height=2)
        self.button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.label = tk.Label(self, text="Did not connect", font=("Arial", 16))
        self.label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        
        self.user_list_label = tk.Label(self, text="Connected Users:")
        self.user_list_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        
        self.user_listbox = tk.Listbox(self)
        self.user_listbox.place(relx=0.5, rely=0.65, anchor=tk.CENTER, width=300, height=150)

        atexit.register(self.cleanup)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.client.update_callback = self.update_ui

        self.request_button = tk.Button(self, text="Send Request", command=self.on_request_button_click, width=20, height=2)
        self.request_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    def on_button_click(self):
        if self.client.connect():
            self.client.request_user_list()
            tk.messagebox.showinfo("Info", "Connected to server. Checking user list...")
        else:
            tk.messagebox.showerror("Error", "Failed to connect to the server.")

    def update_ui(self, client_id_updated=False, request=None, accepted=None):
        if client_id_updated:
            self.after(0, self.update_label)
        if request:
            self.after(0, self.show_request_popup, request)
        if accepted:
            self.after(0, self.show_accepted_popup, accepted)
        self.after(0, self.refresh_user_list)

    def update_label(self):
        if self.client.client_id:
            self.label.config(text=f"You have been assigned the id = {self.client.client_id}")

    def refresh_user_list(self):
        self.user_listbox.delete(0, tk.END)
        for user in self.client.user_list:
            self.user_listbox.insert(tk.END, user)

    def show_request_popup(self, requester_id):
        response = tk.messagebox.askyesno("Request", f"User {requester_id} wants to connect with you. Accept?")
        if response:
            self.client.accept_request(requester_id)
        else:
            print(f"Request from {requester_id} rejected.")

    def show_accepted_popup(self, partner_id):
        tk.messagebox.showinfo("Connection Established", f"You are now connected with {partner_id}")

    def on_request_button_click(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        if selected_user:
            self.client.send_request(selected_user)
        else:
            tk.messagebox.showwarning("Warning", "No user selected.")

    def cleanup(self):
        self.client.disconnect()

    def on_close(self):
        self.cleanup()
        self.destroy()

if __name__ == "__main__":
    client = UDPClient()
    app = Application(client)
    app.mainloop()
