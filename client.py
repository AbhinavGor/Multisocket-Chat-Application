import socket
import select
import errno

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((IP, PORT))

clientSocket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
clientSocket.send(username_header + username)

while True:

    message = input(f'{my_username} > ')

    if message:

        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        clientSocket.send(message_header + message)

    try:
        while True:

            username_header = clientSocket.recv(HEADER_LENGTH)

            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())

            username = clientSocket.recv(username_length).decode('utf-8')

            message_header = clientSocket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = clientSocket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()