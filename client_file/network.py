import socket
import pickle
import time


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.17.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048)) 
        except Exception as e:
            print("Error connecting to the server:", e)
            return None

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data)) 
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print("Error sending/receiving data:", e)
            print("closing")
            self.client.close()
            # time.sleep(1)  # Wait for a moment before attempting to reconnect
            # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.p = self.connect()
            # return None

    def close(self):
        try:
            self.client.close()
            print("Socket closed")
        except Exception as e:
            print("Error closing socket:", e)

