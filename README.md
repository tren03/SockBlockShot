# SockBlockShot

![Screencast](https://github.com/tren03/pyg/assets/82367813/bdbd9769-42c9-4f04-b3eb-273510c6c0e6)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
This project was developed to provide a hands-on understanding of TCP socket programming. The game is designed to run on your local area network (LAN) and demonstrates how to establish connections between clients and a server, and how to send and receive data using TCP sockets.

## Features
- **Multiplayer Support**: Connect multiple clients to the server within the same local network.
- **Real-time Communication**: Players can interact with each other in real-time.
- **Object Serialization**: Uses Python's `pickle` module to serialize and deserialize objects for communication between the server and clients.

## Installation
### Prerequisites
- Python 3.x
- Pygame
- Pickle
- sockets

## Usage
### Starting the Server
1. Navigate to the server directory:
    ```sh
    cd multi_comp
    ```
2. Run the server script: (make sure to change the ip address and port numbers in server and client accordingly)
    ```sh
    python3 server.py
    ```

### Starting the Client
1. Navigate to the client directory:
    ```sh
    cd multi_comp
    ```
2. Run the client script: (If you are only running client on your sytem, make sure to have the network and player class code present locally)
    ```sh
    python client.py
    ```

## How It Works
### Server
The server listens for incoming connections on a specified port. When a client connects, the server spawns a new thread to handle communication with that client, allowing multiple clients to connect simultaneously.

### Client
The client connects to the server using the server's IP address and port number. Once connected, the client can send and receive messages from the server.

### Communication Protocol
The game uses a custom protocol for communication between the client and the server. Messages, including game state updates, are serialized using Python's `pickle` module, ensuring that complex objects can be easily transmitted over the network.

## Technologies Used
- Python
- TCP Sockets
- Threading
- `pickle` for object serialization

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
Special thanks to all the tutorials and open-source projects that provided guidance and inspiration for this project.
