import socket 

HOST = '127.0.0.1'
PORT = 12345 

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM )
server.bind((HOST,PORT))
server.listen()
print(f"[SERVER] Listening on {HOST}:{PORT}...")

conn,addr = server.accept()
print(f"[CONNECTED] Client connected from {addr}")

conn.send("enter your username: ".encode())
username = conn.recv(1024).decode()
print(f"[USERNAME RECEIVED] {username}") 

conn.close()
server.close()


