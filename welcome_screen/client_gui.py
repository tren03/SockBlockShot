import subprocess
import socket
import threading
import tkinter as tk
from tkinter import messagebox
import atexit
import os
import time

class UDPClient:
    def __init__(self, server_ip='172.17.0.1', server_port=5556):
        self.server_address = (server_ip, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_id = None
        self.running = True
        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.user_list = []
        self.update_callback = None
        self.client_process = None

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
                else:
                    print(f"Server response: {decoded_response}")
            except Exception as e:
                print(f"Error: {e}")
                self.disconnect()
                break

    def connect(self):
        if self.client_id is None:
            self.send("CONNECT")
            self.receive_thread.start()
            return self.wait_for_id()

    def wait_for_id(self, timeout=5):
        for _ in range(timeout * 10):
            if self.client_id:
                return True
            time.sleep(0.1)
        return False

    def request_user_list(self):
        self.send("GET")

    def disconnect(self):
        if self.client_id is not None:
            self.send(f"DISCONNECT:{self.client_id}")
        self.running = False
        self.receive_thread.join()
        self.sock.close()
        print("Disconnected from server.")

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
        except Exception as e:
            print(f"Error starting client.py: {e}")


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
        self.button.config(state=tk.DISABLED)
        if self.client.connect():
            self.client.request_user_list()
            tk.messagebox.showinfo("Info", "Connected to server. Checking user list...")
        else:
            tk.messagebox.showerror("Error", "Failed to connect to server.")
            self.button.config(state=tk.NORMAL)
        
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
