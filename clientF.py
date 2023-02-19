import socket
import psutil
import sys

server_ip = sys.argv[1]
port_number = int(sys.argv[2])

def get_usage_info():
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_cores = psutil.cpu_count()
    virtual_memory = psutil.virtual_memory()
    ram_percent = virtual_memory.percent
    disk_usage = psutil.disk_usage('/')
    disk_percent = disk_usage.percent
    usage_info =""
    for i in range(cpu_cores):
        usage_info += f"CPU-{i + 1}: {cpu_percent[i]}%\n"
    usage_info += f"RAM: {ram_percent}%\nDisk: {disk_percent}%"
    return usage_info

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port_number))
    while True:
        usage_info = get_usage_info()
        client_socket.sendall(usage_info.encode())

if __name__ == "__main__":
    main()
