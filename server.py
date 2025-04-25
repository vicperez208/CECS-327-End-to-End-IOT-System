import socket

def main():
    # Get user input, IP, and server_port
    server_host = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port number: "))

    # Create socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_host, server_port))  # Bind Socket
        server_socket.listen(1)  # Listen for incoming connection
        print("Server is listening on", (server_host, server_port))

        client_connection, client_addr = server_socket.accept()
        with client_connection:
            print('Connected by', client_addr)
            while True:
                # Get Data
                data = client_connection.recv(1024).decode()
                if not data:
                    break  # Stop if client disconnects
                if data.lower() == "exit":
                    print("Client disconnected.")
                    break  # End the loop when "exit" is received
                print("Received message:", data)
                
                # Translate data to uppercase
                reply = data.upper()
                client_connection.sendall(reply.encode())  # Send response back

if __name__ == "__main__":
    main()