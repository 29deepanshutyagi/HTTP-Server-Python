---

# HTTP Server Python

This project implements a basic HTTP server in Python capable of handling file requests (GET and POST), supporting content encoding (gzip), and serving responses based on the requested paths.

## Table of Contents

- [Setup and Installation](#setup-and-installation)
- [Running the Server](#running-the-server)
- [Server Features](#server-features)
- [Troubleshooting 404 Errors for File Requests](#troubleshooting-404-errors-for-file-requests)

## Setup and Installation

1. Clone the repository or download the code files.
2. Ensure you have Python 3.x installed.
3. Install any dependencies (if required, you can create a virtual environment):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. No additional dependencies are required for this server.

## Running the Server

To run the server, use the following command, passing the directory you want to serve files from:

```bash
python server.py /path/to/your/files
```

Replace `/path/to/your/files` with the actual path where your files are located.

The server will start running on `localhost` at port `4221`.

## Server Features

- **Root Path (`/`)**: Returns a simple 200 OK response.
- **Echo Path (`/echo/{text}`)**: Echoes the text provided in the URL.
- **User-Agent Path (`/user-agent`)**: Returns the `User-Agent` from the request headers.
- **File Handling (`/files/{filename}`)**:
  - **GET**: Retrieves the specified file from the server directory.
  - **POST**: Saves the content provided in the request body to the specified file in the server directory.

### Example Requests

#### 1. **GET Request (Fetch File)**

To retrieve a file (e.g., `test.txt`):

```bash
curl http://localhost:4221/files/test.txt
```

#### 2. **POST Request (Upload File)**

To upload content to a file (e.g., `test.txt`):

```bash
curl -X POST http://localhost:4221/files/test.txt -d "This is a test content"
```

## Troubleshooting 404 Errors for File Requests

If you're receiving a 404 error when attempting to access files (e.g., `GET /files/test.txt`) via the server, follow these steps to troubleshoot the issue:

### 1. **Check if the file exists in the specified directory**
   Ensure that the file you're trying to access is located in the directory specified when starting the server. For example, if you started the server with the following command:

   ```bash
   python server.py /home/deepanshu/Documents/HTTP-Server-Python/
   ```

   The server will attempt to serve files from the `/home/deepanshu/Documents/HTTP-Server-Python/` directory. Verify that the file you're trying to access (`test.txt` in this case) is in that directory.

   You can check the file's existence with the following command:

   ```bash
   ls /home/deepanshu/Documents/HTTP-Server-Python/test.txt
   ```

   If the file does not exist, you need to place it in the specified directory.

### 2. **Verify file permissions**
   Ensure the file has the appropriate read permissions for the server to access it. You can check the file's permissions with:

   ```bash
   ls -l /home/deepanshu/Documents/HTTP-Server-Python/test.txt
   ```

   Make sure the file has read permissions for the user running the server.

   Example output should show something like this:

   ```bash
   -rw-r--r-- 1 user user 1234 Dec 10 10:00 /home/deepanshu/Documents/HTTP-Server-Python/test.txt
   ```

   If the file does not have the correct permissions, you can update the permissions with:

   ```bash
   chmod 644 /home/deepanshu/Documents/HTTP-Server-Python/test.txt
   ```

### 3. **Verify the constructed file path**
   The server code attempts to open the file using the following logic:

   ```python
   filename = path[7:]  # Removes '/files/' prefix
   ```

   This means that if the request is `GET /files/test.txt`, the server will look for a file named `test.txt` in the directory specified at startup. To help debug, add logging to verify the file path that the server is constructing:

   ```python
   print(f"Requested file path: {os.path.join(directory, filename)}")
   ```

   This will help you confirm that the path the server is trying to access is correct.

### 4. **Test accessing the file directly**
   If you're unsure whether the file is accessible, you can test accessing it directly from the terminal using `cat` to ensure the content is readable:

   ```bash
   cat /home/deepanshu/Documents/HTTP-Server-Python/test.txt
   ```

   If the command successfully outputs the file's content, then the file exists and is readable.

### 5. **Ensure the server's directory exists**
   Double-check that the directory you're passing to the server actually exists. If you provide a non-existent directory, the server will not be able to find any files to serve. You can verify the directory with:

   ```bash
   ls /home/deepanshu/Documents/HTTP-Server-Python/
   ```

### 6. **Common error handling**
   If the server encounters any issues reading the file, it will return a `500 Internal Server Error`. If the file is not found, it will return a `404 Not Found`. Look at the server logs for any error messages that might provide more insight into the problem.

By following these steps, you should be able to resolve the 404 errors when accessing files through the server.

---
