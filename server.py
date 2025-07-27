import socket 
import threading
import os

HOST = '127.0.0.1'
PORT = 12345 

users = {
    "ali" : "1234" , 
    "sara" : "abcd" ,
    "reza" : "pass"
}

user_data={
    "ali" : [] ,
    "sara" : [] ,
    "reza" : []

}

def get_user_file(username):
    return f"{username}.txt"

def load_user_data(username):
    filename = get_user_file(username)
    if os.path.exists(filename):
        with open(filename , "r") as f :
            user_data[username] = [line.strip() for line in f.readlines()] 
    else:
        user_data[username] = []

def save_user_data(username):
        filename = get_user_file(username)
        with open(filename , "w") as f :
            for item in user_data[username] : 
                f.write(item + "\n")

#-----------------------------------------------------------


def handle_add(client_socket , username):
    client_socket.send(b"what would u like to add? ")
    item = client_socket.recv(1024).decode().strip()
    user_data[username].append(item)
    save_user_data(username)
    client_socket.send(b"item add seccessfully\n")
    print(f"[{username}] Added item: {item}")

def handle_get(client_socket , username):
    items = user_data.get(username , [])
    if not items : 
        client_socket.send(b"no items found\n")
    else:
        response = "\n".join(f"{idx+1}. {item}" for idx, item in enumerate(items))
        client_socket.send(response.encode() + b"\n")

def handle_delete(client_socket , username):
    items = user_data.get(username , [])
    if not items : 
        client_socket.send(b"no items to delete.\n")
        return
    response = "\n".join(f"{idx+1}. {item}" for idx, item in enumerate(items))
    client_socket.send(response.encode() + b"\nEnter the number of the item to delete: ")
    try:
        choice = int(client_socket.recv(1024).decode().strip())
        if 1 <= choice <= len(items):
            removed = items.pop(choice - 1)
            save_user_data(username)
            client_socket.send(f"Item '{removed}' deleted successfully.\n".encode())
            print(f"[{username}] Deleted item: {removed}")
        else:
            client_socket.send(b"Invalid choice.\n")
    except ValueError:
        client_socket.send(b"invalid input\n")

def handle_edit(client_socket , username):
    items = user_data.get(username , [])
    if not items :
        client_socket.send(b"no items to edit.\n")
        return
    response = "\n".join(f"{idx+1}. {item}" for idx, item in enumerate(items))
    client_socket.send(response.encode() + b"\n enter the number of item to edit.\n")
    try:
        choice = int(client_socket.recv(1024).decode().strip())
        if 1 <= choice <= len(items) : 
            client_socket.send(b"enter the new value.\n")
            new_value = client_socket.recv(1024).decode().strip()
            old_value = items[choice - 1]
            items[choice - 1] = new_value
            save_user_data(username)
            client_socket.send(b"value update seccessfully.\n")
            print(f"[{username}] Edited item: '{old_value}' to '{new_value}'")
        else:
            client_socket.send(b"invalid choice,\n")
    except ValueError:
        client_socket.send(b"invalid input\n")
#--------------------------------------------------------------------------------

def authenticate(client_socket):
    client_socket.send(b"enter your username:" )
    username = client_socket.recv(1024).decode().strip()

    client_socket.send(b"enter your password: ")
    password = client_socket.recv(1024).decode().strip()

    if username in users and users[username] == password:
        load_user_data(username)
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

        if command == "add" :
            handle_add(client_socket , username)

        if command == "get" : 
            handle_get(client_socket , username)

        if command == "delete" :
            handle_delete(client_socket , username)
        
        if command == "edit" : 
            handle_edit(client_socket , username)


        
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




