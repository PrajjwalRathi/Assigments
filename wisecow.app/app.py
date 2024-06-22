#!/usr/bin/env python3
import socket
import subprocess

SRVPORT = 4499
RSPFILE = 'response'

def get_api():
    line = yield
    yield line

def handleRequest(client_socket, address):
    try:
        # Read the request
        request = client_socket.recv(1024).decode('utf-8')

        # Process the request
        mod = subprocess.check_output(['fortune']).decode('utf-8').strip()
        response = f"HTTP/1.1 200 OK\n\n<pre>`cowsay {mod}`</pre>\n"
        
        # Send the HTTP response
        client_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Exception handling request from {address}: {str(e)}")

    finally:
        client_socket.close()

def main():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_socket.bind(('localhost', SRVPORT))

    # Start listening on the socket
    server_socket.listen(5)
    print(f"Wisdom served on port={SRVPORT}...")

    try:
        while True:
            # Wait for a connection
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")

            # Handle the connection in a separate thread or process
            handleRequest(client_socket, address)

    except KeyboardInterrupt:
        print("\nServer interrupted. Closing...")

    finally:
        # Clean up
        server_socket.close()

if __name__ == "__main__":
    main()
