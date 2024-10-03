# SockBlockShot
## Introduction
This project was developed to provide a hands-on understanding of socket programming. The game is designed to run on your local area network (LAN) and demonstrates how to establish connections between clients and a server, and how to send and receive data using TCP and UDP sockets.

## Demo

Server IP configuration

https://github.com/user-attachments/assets/a6fdc390-a693-404f-941a-039b81c8547c



Actual gameplay

https://github.com/user-attachments/assets/d6abc66c-b8f9-4875-b270-90e7c4c6cd00




## Table of Contents
- [Introduction](#introduction)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)



## Architecture

### The Main Game logic
![image](https://github.com/tren03/SockBlockShot/assets/82367813/f2733cdd-2a28-4ea5-a27e-dd21411080f7)

### The lobby implementation
#### 1. Clients attach to server and obtain ID
![2024-10-03-221624_655x370_scrot](https://github.com/user-attachments/assets/cd7b4043-acaa-4e22-896b-27d9dedea6e1)

#### 2. Client 1 requests to start a session with Client 2
![2024-10-03-221708_708x707_scrot](https://github.com/user-attachments/assets/d7f0c518-1186-4861-8c1a-98346a9f1b70)

#### 3. Managing the game session between Client 1 and 2
![2024-10-03-223729_664x583_scrot](https://github.com/user-attachments/assets/bb0fdddb-36a1-4cbe-9e3f-a9bd5fd57d4e)

#### 4. Ending the game session on 1 Client causes the whole session to end
![2024-10-03-221844_685x764_scrot](https://github.com/user-attachments/assets/6252872b-0c03-403a-ac23-e011d9ed91db)

#### 5. Client disconnection causes a broadcast of the new user list to all clients
![2024-10-03-221852_620x355_scrot](https://github.com/user-attachments/assets/bc302b99-b131-468f-b0ca-3ceb95d546ef)


## Installation
### Prerequisites
- Python 3.x
- Pygame
- Rest of the python modules like pickle, threading etc are built into python

## Usage
### Starting the Server
1. Navigate to the Welcome directory:

    ```sh
    cd welcome_screen
    ```
2. Run the add_server_addr.py: (This changes the ip address of the server socket to match the address of the pc you are running it in)
   
    ```sh
    python3 add_server_addr.py
    ```
3. Run the server_gui.py:
   
    ```sh
    python3 server_gui.py
    ```
4. Run the client_gui.py (can be run on any computer on the lan)
   
     ```sh
    python3 client_gui.py
     ```


### How it works

#### Server
The server listens for incoming UDP connections on a specified port, assigns unique client IDs, and manages multiple clients simultaneously. For each session between clients, a separate subprocess is spawned, and communication within that session is handled using TCP for reliable data transmission.

#### Client
The client connects to the server via UDP using the server’s IP address and port number. Once connected, clients can request sessions with other clients, send/receive messages, and participate in session-based interactions using TCP for the game or communication sessions.

#### Communication Protocol
The project uses UDP for client-server communication and TCP within game sessions for reliable, session-specific communication. The server manages sessions, broadcasts user lists, and handles client requests, ensuring efficient and scalable multiplayer interactions.
