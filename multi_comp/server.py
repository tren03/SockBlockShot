import socket
import pickle
from _thread import *
import atexit
from player1 import Player1
from player2 import Player2

server = "172.17.0.1"
port = 5555
height = 500
width = 500

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

players = [Player1(10, 10, 50, 50, 'red'), Player2(0, height - 50, 50, 50, 'blue')]
clients = []

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    clients.append((conn, addr))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if data == 'LIST':
                reply = clients
            else:
                players[player] = data

                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]

                    print("Received: ", data)
                    print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

def cleanup():
    print("Closing server socket")
    s.close()

atexit.register(cleanup)

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    if currentPlayer > 1:
        currentPlayer = 0
