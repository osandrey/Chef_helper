import socket
import time

TCP_IP = '195.201.150.230'
TCP_PORT = 15000


def run_client():
    ip = TCP_IP
    port = TCP_PORT
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server = ip, port
        sock.connect(server)
        print(f'Connection established {server}')

        user_input = input('Enter the meal: ')
        print(user_input.encode())
        sock.send(user_input.encode())
        time.sleep(2)
        result = sock.recv(1024*10)
        print(result.decode())
        flag = False
        while True:

            if flag:
                user_input = input('Enter the meal: ')
                flag = False
            else:
                user_input = (input('Choose option: '))
                flag = True
            if user_input.lower().strip() == 'exit':
                break
            sock.send(user_input.encode())
            time.sleep(2)
            response = sock.recv(1024 * 10)
            print(f'Response data: {response.decode()}')

    print(f'Data transfer completed')


if __name__ == '__main__':
    run_client()