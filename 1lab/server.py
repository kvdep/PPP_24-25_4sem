import socket
from multiprocessing import Process
from server_functions import client_handler


def start_server(host='127.0.0.1', port=3030):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((host, port))
    
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"{client_address} connected.")
            
            #reading an str for client_handler(arg)
            data = ''
            part=''
            while part:
                data+= part
                part = client_socket.recv(1024).decode('utf-8')
            print('Packet recieved')

            process = Process(target=client_handler, args=(data,))
            process.start()
            client_socket.close()
    except KeyboardInterrupt:
        print("Server paused")
    finally:
        server_socket.close()