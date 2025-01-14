import os
import subprocess
import time
import http.server
import socketserver

# Automatically find an available port
def find_free_port():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# Start the HTTP server
def start_server(port):
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print(f"Serving on port {port}")
    httpd.serve_forever()

# Start LocalTunnel and get the public URL
def start_localtunnel(port):
    # Run localtunnel to get a public URL
    lt_command = f"lt --port {port}"
    process = subprocess.Popen(lt_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for the tunnel to establish and print the URL
    print("Connecting to LocalTunnel...")
    time.sleep(5)  # Wait for LocalTunnel to connect
    output, error = process.communicate()
    
    if error:
        print(f"Error: {error.decode()}")
    else:
        # Look for the public URL in the output
        for line in output.decode().splitlines():
            if "your subdomain" in line:
                print(f"Your public link is: {line.strip()}")

if __name__ == "__main__":
    # Find an available port
    port = find_free_port()
    
    # Start the local server
    print("Starting local server...")
    start_server(port)

    # Start LocalTunnel and get the public URL
    start_localtunnel(port)
