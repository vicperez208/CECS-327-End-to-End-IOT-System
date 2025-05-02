import socket

def main():
    host = input("Enter the server IP address: ")
    port = int(input("Enter the server port number: "))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"\n Connected to server at {host}:{port}\n")
    except Exception as e:
        print(f" Error connecting to server: {e}")
        return

    while True:
        print("Select a query:")
        print("1: Average moisture inside the fridge in the last 3 hours")
        print("2: Average water consumption per dishwasher cycle")
        print("3: Device with the highest electricity consumption")
        print("Type 'exit' to close the client\n")

        query = input("Enter your choice (1, 2, 3, or exit): ").strip()

        if query.lower() == "exit":
            print(" Closing the client.")
            client_socket.sendall(query.encode())
            break

        if query not in ["1", "2", "3"]:
            print(" Invalid input. Please enter 1, 2, 3, or exit.")
            continue

        try:
            client_socket.sendall(query.encode())
            response = client_socket.recv(4096).decode()
            print(f"\n Response from server:\n{response}\n")
        except Exception as e:
            print(f" Communication error: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
