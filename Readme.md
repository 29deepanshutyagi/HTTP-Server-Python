# HTTP-Server-Python

## Project Overview
A simple custom HTTP/1.1 server built using Python 3.11 that handles multiple clients concurrently using TCP/IP networking. The server supports handling different HTTP requests, such as echoing text, returning the user agent, and managing files (both GET and POST requests).

### Features:
- Serve static content
- Echo service for GET requests on `/echo/`
- Return the user-agent of the client
- Support for GZIP compression
- File handling (GET and POST methods)
- Multi-client architecture using threads

## Usage
1. Clone this repository.
2. To run the server, use the command:
   ```bash
   python server.py <directory>
