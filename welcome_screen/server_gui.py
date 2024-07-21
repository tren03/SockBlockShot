import subprocess
import socket
import threading
import time

class UDPServer:
    def __init__(self, host='172.17.0.1', port=5556):
        self.server_address = (host, port)
        self.active_clients = {}  # Use a dictionary to store client addresses and IDs
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.server_address)
        print(f"Server is listening on {self.server_address}")

    def broadcast_user_list(self):
        user_list = ",".join(self.active_clients.values())
        message = f"USERLIST:{user_list}"
        for address in self.active_clients.keys():
            self.sock.sendto(message.encode(), address)

    def handle_client(self):
        client_id_counter = 1
        while True:
            try:
                message, client_address = self.sock.recvfrom(4096)
                message = message.decode()

                if message == "GET":
                    self.broadcast_user_list()
                elif message.startswith("CONNECT"):
                    if client_address not in self.active_clients:
                        client_id = f"Client{client_id_counter}"
                        self.active_clients[client_address] = client_id
                        client_id_counter += 1
                        response = f"ID:{client_id}"
                        print(f"Client {client_address} connected with ID {client_id}.")
                        self.broadcast_user_list()
                        self.sock.sendto(response.encode(), client_address)
                elif message.startswith("DISCONNECT"):
                    client_id = message.split(":")[1]
                    if client_address in self.active_clients and self.active_clients[client_address] == client_id:
                        del self.active_clients[client_address]
                        print(f"Client {client_address} with ID {client_id} disconnected.")
                        self.broadcast_user_list()
                elif message.startswith("REQUEST"):
                    _, requester_id, target_id = message.split(":")
                    target_address = next((addr for addr, cid in self.active_clients.items() if cid == target_id), None)
                    if target_address:
                        self.sock.sendto(f"REQUEST:{requester_id}".encode(), target_address)
                elif message.startswith("ACCEPT"):
                    _, acceptor_id, requester_id = message.split(":")
                    requester_address = next((addr for addr, cid in self.active_clients.items() if cid == requester_id), None)
                    if requester_address:
                        self.sock.sendto(f"ACCEPT:{acceptor_id}".encode(), requester_address)
                        self.sock.sendto(f"ACCEPT:{requester_id}".encode(), client_address)
                        # Start server.py
                        self.start_server_process()
                        # Notify clients to start their own client.py
                        time.sleep(2)
                        self.notify_clients_to_start_client()
                else:
                    print(f"Received message from {client_address}: {message}")

                response = "Message received"
                self.sock.sendto(response.encode(), client_address)
                print(f"Number of unique clients: {len(self.active_clients)}")
            except Exception as e:
                print(f"Error: {e}")

    def start_server_process(self):
        try:
            subprocess.Popen(['python3', '../multi_comp/server.py'])
            print("Started server.py")
        except Exception as e:
            print(f"Error starting server.py: {e}")

    def notify_clients_to_start_client(self):
        message = "START_CLIENT"
        for address in self.active_clients.keys():
            self.sock.sendto(message.encode(), address)

    def start(self):
        try:
            self.handle_client()
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            self.sock.close()

if __name__ == "__main__":
    server = UDPServer()
    server.start()
