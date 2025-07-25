import socket 
import threading

HOST = '127.0.0.1'
PORT = 12345 

users = {
    "ali" : "1234" , 
    "sara" : "abcd" ,
    "reza" : "pass"
}

def authenticate(client_socket):
    client_socket.send(b"enter your username:" )
    username = client_socket.recv(1024).decode().strip()

    client_socket.send(b"enter your password: ")
    password = client_socket.recv(1024).decode().strip()

    if username in users and users[username] == password:
        client_socket.send(b"Authentication successful!\n")
        print(f"[AUTH] User '{username}' authenticated successfully.")
        return True, username
    else:
        client_socket.send(b"Authentication failed. Closing connection.\n")
        print(f"[AUTH] Failed authentication attempt for user '{username}'.")
        return False, username


def handle_client(client_socket , addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    seccess , username = authenticate(client_socket)
    if not seccess:
        client_socket.close()
        return
    while True :
        client_socket.send(b"\nEnter command (add/edit/get/delete/quit): ")
        command = client_socket.recv(1024).decode().strip()

        valid_commands = ["add" , "edit" , "get" , "delete" , "quit"]

        if command not in valid_commands:
            client_socket.send(b"Invalid command. Try again.\n")
            continue
        
        if command == "quit":
            client_socket.send(b"goodbye\n")
            break
        print(f"[{username}@{addr}] Command received: {command}")
        client_socket.send(b"Command received.\n")
    client_socket.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

        


server = socket.socket(socket.AF_INET , socket.SOCK_STREAM )
server.bind((HOST,PORT))
server.listen()
print(f"[SERVER] Listening on {HOST}:{PORT}...")

while True : 
    client_socket , addr = server.accept()
    thread = threading.Thread(target = handle_client , args=(client_socket , addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")




