import socket
from multiprocessing import Process
from server_functions import client_handler
from server_functions import init

init()


def client_handler_server(data, sock):
    result = client_handler(data)
    sock.sendall(result[0].encode("utf-8"))
    try:
        sock.sendall(result[1].encode("utf-8"))
    except:
        pass
    #sock.sendall(result[0])
    #sock.sendall(result[1])
    print("Results sent! Closing socket")
    sock.shutdown(socket.SHUT_WR)
    sock.close()


def start_server(host="127.0.0.1", port=57394):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"{client_address} connected.")

            # reading an str for client_handler(arg)
            data = ""
            part = client_socket.recv(1024).decode("utf-8")
            print("Recieving package")
            while part:
                data += part
                part = client_socket.recv(1024).decode("utf-8")
                print(data)
            print(f"Packet recieved: {data}")

            process = Process(
                target=client_handler_server,
                args=(
                    data,
                    client_socket,
                ),
            )
            process.start()
            # client_socket.close()
    except KeyboardInterrupt:
        print("Server paused")
    finally:
        server_socket.close()
