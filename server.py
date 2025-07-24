import socket 

HOST = '127.0.0.1'
PORT = 12345 

authorized_users = ['ali', 'sara', 'mohammad']


server = socket.socket(socket.AF_INET , socket.SOCK_STREAM )
server.bind((HOST,PORT))
server.listen()
print(f"[SERVER] Listening on {HOST}:{PORT}...")

conn,addr = server.accept()
print(f"[CONNECTED] Client connected from {addr}")

conn.send("enter your username: ".encode())
username = conn.recv(1024).decode()
print(f"[USERNAME RECEIVED] {username}") 

if username in authorized_users : 
    conn.send("Authentication successful".encode())
    print(f"[AUTH] User '{username}' authenticated.")
else:
    conn.send("Authentication failed".encode())
    print(f"[AUTH] User '{username}' failed authentication.")
    conn.close()

conn.close()
server.close()


