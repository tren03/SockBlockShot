import subprocess
import time

def run_server():
    # Start the server process
    server_process = subprocess.Popen(['python3', 'server.py'])
    return server_process

def run_client():
    # Start a client process
    client_process = subprocess.Popen(['python3', 'client.py'])
    return client_process

def main():
    # Start the server
    server_process = run_server()
    print("Server started...")

    # Allow some time for the server to start up
    time.sleep(2)

    # Start two clients
    client1_process = run_client()
    client2_process = run_client()
    print("Client 1 and Client 2 started...")

    try:
        # Wait for the clients to finish (this is just an example, you may need to adjust this)
        client1_process.wait()
        client2_process.wait()
    except KeyboardInterrupt:
        print("Terminating processes...")

    finally:
        # Ensure all processes are terminated
        server_process.terminate()
        client1_process.terminate()
        client2_process.terminate()
        print("Processes terminated.")

if __name__ == "__main__":
    main()
