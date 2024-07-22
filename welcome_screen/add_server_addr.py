import tkinter as tk
from tkinter import messagebox
import re
import json

# Function to validate IP address
def is_valid_ip(ip):
    pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    return re.match(pattern, ip) is not None

# Function to handle the submission
def submit():
    global server_addr
    server_addr = entry.get()
    if server_addr:
        if is_valid_ip(server_addr):
            # Write the server address to the config file
            with open('../config/config.json', 'w') as f:
                json.dump({"server_address": server_addr}, f)
            messagebox.showinfo("Information", "Thank you! The server address has been recorded.")
            root.destroy()  # Close the window
        else:
            messagebox.showwarning("Warning", "Invalid IP address. Please enter a valid IPv4 address.")
    else:
        messagebox.showwarning("Warning", "Please enter a server address.")

# Create the main window
root = tk.Tk()
root.title("Server Address Input")

# Create and place a label
label = tk.Label(root, text="Enter Server Address (IPv4):")
label.pack(pady=10)

# Create and place a text entry widget
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Create and place a submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
