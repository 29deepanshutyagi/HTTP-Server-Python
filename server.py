import socket
import threading
import sys
import gzip
import os

def handle_connection(sock, addr):
    req = sock.recv(1024).decode()

    # Print the request for debugging
    print(f"Received request: {req}")

    # Extract path from request
    path = req.split("\r\n")[0].split(" ")[1]
    
    # Extract headers
    headers = req.split("\r\n")[1:]
    encoding = None
    for header in headers:
        if "Accept-Encoding" in header:
            encoding = header.split(":")[1].strip()

    # Handle root path
    if path == "/":
        sock.send(b'HTTP/1.1 200 OK\r\n\r\n')

    # Handle echo path
    elif path.startswith("/echo/"):
        content = path[6:]
        if encoding == "gzip" and "gzip" in encoding:
            compressed_content = gzip.compress(content.encode())
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {len(compressed_content)}\r\n\r\n"
            sock.send(response.encode() + compressed_content)
        else:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
            sock.send(response.encode())

    # Handle user-agent path
    elif path.startswith("/user-agent"):
        user_agent = None
        for line in req.split("\r\n"):
            if line.startswith("User-Agent:"):
                user_agent = line.split("User-Agent:")[1].strip()
                break
        
        if encoding == "gzip" and "gzip" in encoding:
            compressed_content = gzip.compress(user_agent.encode())
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {len(compressed_content)}\r\n\r\n"
            sock.send(response.encode() + compressed_content)
        else:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
            sock.send(response.encode())

    # Handle file operations
    elif path.startswith("/files"):
        method = req.split("\r\n")[0].split(" ")[0]
        directory = sys.argv[1]  # Directory passed as first argument

        # GET file request
        if method == "GET":
            filename = path[7:]  # Remove '/files/' prefix
            try:
                file_path = os.path.join(directory, filename)
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        body = f.read()
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n"
                        sock.send(response.encode() + body.encode())
                else:
                    response = f"HTTP/1.1 404 Not Found\r\n\r\n"
                    sock.send(response.encode())
            except Exception as e:
                print(f"Error reading file: {e}")
                response = f"HTTP/1.1 500 Internal Server Error\r\n\r\n"
                sock.send(response.encode())

        # POST file request
        elif method == "POST":
            filename = path[7:]  # Remove '/files/' prefix
            try:
                body = req.split("\r\n\r\n")[1]  # Get the body of the request
                file_path = os.path.join(directory, filename)
                with open(file_path, "w") as f:
                    f.write(body)
                response = f"HTTP/1.1 201 Created\r\n\r\n"
                sock.send(response.encode())
            except Exception as e:
                print(f"Error writing file: {e}")
                response = f"HTTP/1.1 500 Internal Server Error\r\n\r\n"
                sock.send(response.encode())

    # Handle 404 for unknown paths
    else:
        sock.send(b'HTTP/1.1 404 Not Found\r\n\r\n')

    sock.close()

def main():
    if len(sys.argv) < 2:
        print("Error: Please provide the directory as a command-line argument.")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.exists(directory):
        print(f"Error: The directory {directory} does not exist.")
        sys.exit(1)

    print("Server is running...")

    # Create server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    # Accept client connections in a loop
    while True:
        sock, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(sock, addr))
        thread.start()

if __name__ == "__main__":
    main()
