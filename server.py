import socket
import psycopg2
import json

# Database connection configuration
DB_URL = "postgresql://327test_owner:npg_6YjBoaERdtw7@ep-dawn-frost-a5220y23-pooler.us-east-2.aws.neon.tech/327test?sslmode=require"

def fetch_latest_payload():
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT payload FROM dataniz_data_virtual ORDER BY (payload ->> 'timestamp')::bigint DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            payload = row[0]  # Get the payload (already a JSON object in dictionary format)
            if isinstance(payload, str):  # If it's a string, parse it as JSON
                return json.loads(payload)
            return payload  # If it's already a dictionary, return it as is
        else:
            return None
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def process_query(option):
    payload = fetch_latest_payload()

    if payload is None:
        return "No data found."

    if isinstance(payload, dict) and "error" in payload:
        return f"Database error: {payload['error']}"

    print("Fetched Payload:", payload)
    print("Keys in Payload:", payload.keys())

    if option == "1":
        # Search for a key related to moisture
        moisture_key = next((k for k in payload if 'moisture' in k.lower()), None)
        if moisture_key:
            moistures = [float(moisture) for moisture in payload[moisture_key] if moisture is not None]

            if len(moistures) > 0:
                avg = sum(moistures) / len(moistures)
                return f"Average Moisture inside the fridge (Last 3 hours): {avg:.2f}%"
            else:
                return "No moisture data available for the last 3 hours."
        else:
            return "Moisture data not available in current schema."

    elif option == "2":
        # Check for a key specifically related to water consumption, e.g., "Water consumption sensor"
        water_key = next((k for k in payload if 'Water consumption sensor' in k), None)
        
        if water_key:
            # If found, return the water consumption value
            return f"Water Consumption: {payload[water_key]} L"
        else:
            # If no specific key is found, fall back to average sensor values
            sensor_keys = [k for k in payload if 'sensor' in k.lower()]
            if sensor_keys:
                sensor_values = [float(payload[k]) for k in sensor_keys if payload[k] is not None]
                
                if len(sensor_values) > 0:
                    avg_sensor_value = sum(sensor_values) / len(sensor_values)
                    return f"Average Sensor Value: {avg_sensor_value:.2f}"
                else:
                    return "No sensor data available."
            else:
                return "Water consumption data not available."

    elif option == "3":
        # Check for a key related to ammeter/electricity
        ammeter_key = next((k for k in payload if 'ammeter' in k.lower()), None)
        board_name = payload.get('board_name', 'N/A')
        if ammeter_key:
            return f"Highest Electricity Consuming Device (Recent): {board_name} at {payload[ammeter_key]} A"
        else:
            return f"Highest Electricity Consuming Device (Recent): {board_name} at N/A A"

    else:
        return "Invalid option."





def main():
    server_host = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port number: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_host, server_port))
        server_socket.listen(1)
        print("Server is listening on", (server_host, server_port))

        client_connection, client_addr = server_socket.accept()
        with client_connection:
            print('Connected by', client_addr)
            while True:
                data = client_connection.recv(1024).decode()
                if not data:
                    break
                if data.lower() == "exit":
                    print("Client disconnected.")
                    break

                print("Received message:", data)

                if data in ["1", "2", "3"]:
                    reply = process_query(data)
                else:
                    reply = "Invalid input."

                client_connection.sendall(reply.encode())

if __name__ == "__main__":
    main()
