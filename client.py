import socket

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))  
msg = client.recv(1024).decode()
print(msg)

username = input(">>> ")
client.send(username.encode())

client.close()
