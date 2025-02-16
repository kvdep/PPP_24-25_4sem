import socket

def send_request_to_server(message, host='127.0.0.1', port=57394):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected a server with this adress: {host}:{port}")
            client_socket.sendall(message.encode('utf-8'))
            print(f"Message sent to {host}:{port}")
            client_socket.shutdown(socket.SHUT_WR)

    
            data = client_socket.recv(1024)
            print(f"Message recieved: {data.decode('utf-8')}")
        


message = """
select name as name
from cities as c
where name != city
"""
message="""city1|name,age,city
Alice,30,New York
Bob,25,Los Angeles
Charlie,35,Chicago"""
message = """
select name as name
from city1 as c
where name != city
"""
print(message)
send_request_to_server(message)