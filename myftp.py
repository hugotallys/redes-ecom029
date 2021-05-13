import os
import sys
import socket

from utils import default_route_ip, SEPARATOR, BUFFER_SIZE


class FTPClient:

    name = default_route_ip()

    def __init__(self, server_port, server_name):

        self.server_port = server_port
        self.server_name = server_name
        self.client_socket = None

    def connect(self):
        """
        Connects to the server (3-way presentation).
        """
        # Creates the client socket specifying the family (AF_INET ipv4)
        # and making explicit that it is a TCP socket (SOCK_STREAM).
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_name, self.server_port))

    def send_to_server(self, bytes):
        """
        Sends bytes via client socket and to the TCP connection.
        """
        self.client_socket.send(bytes)

    def put_to_server(self, message, filename):
        """
        Puts local file in the server.
        """
        with open(filename, "rb") as file:
            message = bytes(message + SEPARATOR + SEPARATOR, "utf-8")

            ftp_client.client_socket.sendall(message)

            chunk = file.read(BUFFER_SIZE)

            while chunk != b"":

                ftp_client.client_socket.sendall(chunk)

                chunk = file.read(BUFFER_SIZE)

    def recieve_from_server(self):
        """
        Recieves bytes from the server and through the TCP connection.
        """
        # Maximum amount of data to be received at once.
        return self.client_socket.recv(BUFFER_SIZE)

    def terminate(self):
        """
        Terminates the session with the server.
        """
        self.client_socket.close()

    def parse_command(self, command):
        """
        Breaks the command in two components: the command itself
        and parameter (if any).

        :param command: The input string representing the command.
        """
        parsed = command.strip(" ").split(" ")

        if len(parsed) == 1:
            return parsed[0], ""
        else:
            return parsed[0], parsed[1]

    def format_message(self, cmd, param, file_size=0):

        return (
            f"ClientName:{self.name}{SEPARATOR}Command:{cmd}{SEPARATOR}"
            f"Parameter:{param}{SEPARATOR}FileSize:{file_size}"
        )


if __name__ == "__main__":

    try:
        server_name = sys.argv[1]
        port_number = sys.argv[2]
    except IndexError:
        raise IndexError(
            (
                "Parameter <server_name> or <port_number> is missing. "
                "To execute this program run:\n"
                "$ python myftp.py <server_name> <port_number>"
            )
        )

    ftp_client = FTPClient(
        server_name=server_name, server_port=int(port_number)
    )

    command = input("myftp>")
    cmd, param = ftp_client.parse_command(command=command)

    while cmd != "quit":

        ftp_client.connect()

        if cmd == "put":
            file_size = os.path.getsize(param)
            message = ftp_client.format_message(
                cmd, param, file_size
            )
            ftp_client.put_to_server(message, param)
        else:
            message = ftp_client.format_message(cmd, param)
            ftp_client.send_to_server(bytes=bytes(message, "utf-8"))

        server_response = ftp_client.recieve_from_server()

        # Outputs message on screen.
        print(server_response.decode("utf-8"))

        command = input("myftp>")
        cmd, param = ftp_client.parse_command(command=command)

    ftp_client.terminate()

    print("Bye!")
