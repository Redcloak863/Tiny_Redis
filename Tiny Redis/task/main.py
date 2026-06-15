# Write your solution here
import socket  # The TCP server
import sys
import bulk_string

# server_socket = socket.socket()
host = '0.0.0.0'
port = 6379  # The Redis default port.


pong = '+PONG\r\n'.encode()  # The standard Redis 'PONG' response in bytes.
error_string = '-Parsing error!\r\n'.encode()

def main():
    # Call your server handling logic here
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        while True:
            server_socket.listen(5)  # Listen for the connection

            while True:
                conn, addr = server_socket.accept()  # Establish the new connection
                with conn:

                    data_in = conn.recv(1024)
                    data_in = data_in.decode()
                    # print(data_in)

                    if data_in == '+PING\r\n':
                        conn.send(pong)
                        # print(f'Sent {pong}.')
                        break
                        # print(pong)
                    elif data_in == '+EXIT\r\n':
                        # print(f'Received exit command.')
                        sys.exit()

                    else:
                        conn.send(error_string)
                        # print(f'Sent {error_string}.')
                    # At this point, the loop should begin again looking for a new connection

if __name__ == "__main__":
    main()