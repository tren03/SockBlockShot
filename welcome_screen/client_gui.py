import socket
import threading
import tkinter as tk
from tkinter import messagebox
import atexit
import sys

class UDPClient:
    def __init__(self, server_ip='172.17.0.1', server_port=5556):
        self.server_address = (server_ip, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_id = None
        self.running = True
        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.user_list = []
        self.update_callback = None  # Callback to update the UI

    def send(self, message):
        self.sock.sendto(message.encode(), self.server_address)

    def receive(self):
        while self.running:
            try:
                response, _ = self.sock.recvfrom(4096)
                decoded_response = response.decode()
                if decoded_response.startswith("ID:"):
                    # Extract and store the client ID
                    self.client_id = decoded_response.split(":")[1]
                    print(f"Assigned ID: {self.client_id}")
                    # Call the update callback to refresh the UI
                    if self.update_callback:
                        self.update_callback(client_id_updated=True)
                elif decoded_response.startswith("USERLIST:"):
                    # Update user list
                    self.user_list = decoded_response.split(":")[1].split(",") if decoded_response.split(":")[1] else []
                    print(f"Updated user list: {self.user_list}")
                    # Call the update callback to refresh the UI
                    if self.update_callback:
                        self.update_callback(client_id_updated=False)
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
        
    def request_user_list(self):
        self.send("GET")
        
    def disconnect(self):
        if self.client_id is not None:
            self.send(f"DISCONNECT:{self.client_id}")
        self.running = False
        self.receive_thread.join()  # Wait for the receive thread to stop
        self.sock.close()
        print("Disconnected from server.")


class Application(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.title("Tkinter Button Example")
        self.geometry("400x300")
        
        self.client = client
        
        # Create a button to connect to the server
        self.button = tk.Button(self, text="Connect to the server", command=self.on_button_click, width=20, height=2)
        self.button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Create a label to display connection status
        self.label = tk.Label(self, text="Did not connect", font=("Arial", 16))
        self.label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        
        # Create a label and listbox to display the user list
        self.user_list_label = tk.Label(self, text="Connected Users:")
        self.user_list_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        
        self.user_listbox = tk.Listbox(self)
        self.user_listbox.place(relx=0.5, rely=0.65, anchor=tk.CENTER, width=300, height=150)

        # Register cleanup function to be called on exit
        atexit.register(self.cleanup)

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set the update callback for the client
        self.client.update_callback = self.update_ui

    def on_button_click(self):
        self.client.connect()
        self.client.request_user_list()
        tk.messagebox.showinfo("Info", "Connected to server. Checking user list...")
        
    def update_ui(self, client_id_updated):
        if client_id_updated:
            self.after(0, self.update_label)  # Update label with client ID
        self.after(0, self.refresh_user_list)  # Update user list

    def update_label(self):
        # Update the label text with the new client ID
        if self.client.client_id:
            self.label.config(text=f"You have been assigned the id = {self.client.client_id}")

    def refresh_user_list(self):
        # Clear the listbox and populate it with the new user list
        self.user_listbox.delete(0, tk.END)
        for user in self.client.user_list:
            self.user_listbox.insert(tk.END, user)

    def on_close(self):
        # Ensure disconnect is called when the window is closed
        self.cleanup()
        self.destroy()

    def cleanup(self):
        # Call the disconnect method of UDPClient
        if self.client:
            self.client.disconnect()

if __name__ == "__main__":
    client = UDPClient()
    app = Application(client)
    
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        # Ensure cleanup is called if program is terminated abruptly
        client.disconnect()
        sys.exit()
