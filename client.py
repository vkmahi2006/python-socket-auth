import socket

HOST = '127.0.0.1'
PORT = 12345
def recv_full_msg(sock):
    try:
        data = sock.recv(1024)
        if not data:
            return ''
        return data.decode()
    except:
        return ''

    

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client_socket.connect((HOST, PORT)) 

    print(recv_full_msg(client_socket), end='')
    username = input()
    client_socket.send(username.encode())
    print(recv_full_msg(client_socket), end='')
    password = input()
    client_socket.send(password.encode())
    auth_result = recv_full_msg(client_socket)
    print(auth_result)

    if "successful" not in auth_result:
        print("Authentication failed, closing connection.")
        client_socket.close()
        return

    while True:  
        prompt = recv_full_msg(client_socket)
        #print(prompt , end = '')
        command = input("\nEnter command (add/edit/get/delete/quit): ")
        client_socket.send(command.encode())

        if command == "quit":
            print(recv_full_msg(client_socket))
            break

        while True:
            response = recv_full_msg(client_socket)
            if not response:
                break
            print(response, end='')
            if any(phrase in response.lower() for phrase in [
                "what would u like to add",
                "enter the number",
                "enter the new value"
            ]):
                user_input = input()
                client_socket.send(user_input.encode())
            else:
                break


    client_socket.close()

if __name__ == "__main__":
    main()








