import socket

HOST = '127.0.0.1'
PORT = 12345

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client_socket.connect((HOST, PORT)) 

    message = client_socket.recv(1024).decode()
    print(message, end='')

    username = input()
    client_socket.send(username.encode())  

    message = client_socket.recv(1024).decode()
    print(message, end='')

    password = input()
    client_socket.send(password.encode())

    auth_result = client_socket.recv(1024).decode()
    print(auth_result)

    if "successful" not in auth_result:
        print("Authentication failed, closing connection.")
        client_socket.close()
        return

    while True:  
        command = input("\nEnter command (add/edit/get/delete/quit): ")
        client_socket.send(command.encode())

        if command == "quit":
            print("Disconnecting from server.")
            break

        response = client_socket.recv(1024).decode()
        print(f"Response from server: [{response.strip()}]")

    client_socket.close()

if __name__ == "__main__":
    main()








