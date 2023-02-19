import socket
import threading
import time
import sys

# take arguments when calling from cmd
port_number = int(sys.argv[1])
max_clients = int(sys.argv[2])
report_time = int(sys.argv[3])


stored_clients = [None] * max_clients
def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def print_latest_usage_info(stored_clients):
    while True:
        latest_usage = {}
        time.sleep(report_time)
        for i, usage_info in enumerate(stored_clients):
            if usage_info is not None:
                latest_usage[i+1] = usage_info
        for i, usage_info in latest_usage.items():
            print(f"Client-{i} Usage Info:")
            print(usage_info)
        latest_usage.clear()

def handle_client(client_socket, client_number):
    while True:
        usage_info = client_socket.recv(1024).decode()
        if not usage_info:
            break
        stored_clients[client_number-1] = usage_info
        

def main():
    client_number = 1
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = get_internal_ip()
    server_socket.bind((ip_address, port_number))

    server_socket.listen(client_number)
    print(f"==== Server is listening!({ip_address}) =====")

    print_thread = threading.Thread(target=print_latest_usage_info, args=(stored_clients,))
    print_thread.start()

    while client_number <= max_clients:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_number))
        client_thread.start()
        client_number += 1


if __name__ == "__main__":
    main()
