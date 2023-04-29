import socket
import time
from concurrent import futures as cf
from reciept_searcher_service import get_reciept_by_name, get_reciept_via_id, get_logger

# TCP_IP = '0.0.0.0' #for server
TCP_IP = 'localhost' #for local
TCP_PORT = 15000
logger = get_logger(__name__)

def run_server(ip, port):
    def handle(sock: socket.socket, address: str):
        logger.debug('Start program!')
        print(f'Connection established {address}')

        while True:
            received = sock.recv(1024*10)
            if not received:
                break
            data = received.decode()
            print(data)
            if data.isdigit():
                continue
            results = get_reciept_by_name(data)
            print(results)
            meals_variation = dict()
            option = 1
            sock_send_data = ''
            for item in results:
                print(item)
                meals_variation[option] = (item.get('id'))
                sock_send_data += f'Option {option} (-_-)-> {item.get("title")}\n'
                option += 1
            sock.send(sock_send_data.encode())
            time.sleep(2)
            id_num = sock.recv(1024*10)
            print(id_num)
            if id_num.decode().isdigit():
                target_id = meals_variation[int(id_num.decode())]
                title, instruction = get_reciept_via_id(target_id)
                print(title, instruction, sep=' | ')
                sock.send(f'Your meal is: {title}\nThe coocking: {instruction}'.encode())
                logger.info(f'Your meal is: {title}\n')
                logger.warning(f'The coocking: {instruction}\n')
                time.sleep(2)
            else:
                sock.send(f'Please choose digit type integer (1-10)')



            # sock.send(received)
        print(f'Socket connection closed {address}')
        sock.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)
    print(f'Start echo server {server_socket.getsockname()}')
    with cf.ThreadPoolExecutor(10) as client_pool:
        try:
            while True:
                new_sock, address = server_socket.accept()
                client_pool.submit(handle, new_sock, address)
        except KeyboardInterrupt:
            print(f'Destroy server')
        finally:
            server_socket.close()


if __name__ == '__main__':
    run_server(TCP_IP, TCP_PORT)