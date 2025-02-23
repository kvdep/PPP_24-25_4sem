import socket


def send_request_to_server(message, host="127.0.0.1", port=57394):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected a server with this adress: {host}:{port}")
        client_socket.sendall(message.encode("utf-8"))
        print(f"Message sent to {host}:{port}")
        client_socket.shutdown(socket.SHUT_WR)

        #data = client_socket.recv(1024)
        data = ""
        part = client_socket.recv(1024).decode("utf-8")
        print("Recieving package")
        while part:
            data += part
            part = client_socket.recv(1024).decode("utf-8")
            #print(data)
        #print(f"Packet recieved: {data}")
        print(f"Packet recieved.")

        #обработаем запрос 
        status = data[:data.find('.')]
        body = data[data.find('.')+1:]
        return (status,body)
        #print(f"Message recieved: {status}")

def start_client(host="127.0.0.1", port=57394):
    print('Client initiated, standby.\n')
    print(f'Available commands:\n')
    print(f'JSON_IT <=> вывод json файла с названиям таблиц и их столбцами\nSELECT/select ... from ... where(optional) ... <=> select-запрос\nНазвание|Файл <=> запись csv файла')
    while True:
        message = input("\nEnter your request (or 'shutdown' to quit):\n")
        if message.strip().lower()[:8] == 'shutdown':
            print("Exiting client.")
            break
        while (message.strip()[-1]!=';'):
            message+=input()
        

        print('\nEstablishing connection to server.\n')
        status,body = send_request_to_server(message,host,port)
        print(f'Inquiry status: {status}')
        if status=='Success':
            print(f'------------------------\n')
            print(body)
            print(f'\n------------------------\n')




        

message = """
select name as name
from cities as c
where name != city
"""
message = """city1|name,age,city
Alice,30,New York
Bob,25,Los Angeles
Charlie,35,Chicago"""
message = """
select name as name
from city1 as c
where name != city
"""

# s = JSON_IT <=> JSON_IT - вывод json файла с названиям таблиц и их столбцами
# s = SELECT/select ... from ... where(optional) ...<=> select-запрос
# s = Название|Файл <=> запись csv файла


#print(message)
#send_request_to_server(message)
start_client()