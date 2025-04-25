import socket

def get_server_info():
    while True:
        # Get user input, IP and Port
        server_ip = input("Enter the server IP address: ")
        server_port = input("Enter the server port number: ")

        if not server_port.isdigit():
            print("Port number should be a positive integer.")
            continue

        return server_ip, int(server_port)

def main():
    # Get server IP and port from user
    server_ip, server_port = get_server_info()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((server_ip, server_port))  # Connect to server
            
            while True:
                # Prompt user to enter a message
                message = input("Enter a message to send to the server (type 'exit' to quit): ")
                server_socket.sendall(message.encode())  # Send message
                
                if message.lower() == "exit":
                    print("Closing connection...")
                    break  # Exit loop if "exit" is sent

                # Receive the message from the server
                data = server_socket.recv(1024)
                print("Server reply:", data.decode())

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()