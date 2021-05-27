import os
import ast
import sys
import socket
import utils


class FTPClient:

    def __init__(self, server_port, server_name):

        self.server_port = server_port
        self.server_name = server_name
        self.client_socket = None
        self.name = None

    def connect(self):
        """
        Connects to the server (3-way presentation).
        """
        # Creates the client socket specifying the family (AF_INET ipv4)
        # and making explicit that it is a TCP socket (SOCK_STREAM).
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_name, self.server_port))

        addr, port = self.client_socket.getsockname()
        self.name = f"{addr}:{port}"

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
            message = bytes(message, "utf-8")

            ftp_client.client_socket.sendall(message)

            chunk = file.read(utils.BUFFER_SIZE)

            while chunk != b"":

                ftp_client.client_socket.sendall(chunk)

                chunk = file.read(utils.BUFFER_SIZE)

    def recieve_from_server(self, filename):
        """
        Recieves bytes from the server and through the TCP connection.
        """

        message = self.client_socket.recv(utils.BUFFER_SIZE)

        file_transer, response = self.parse_message(message)

        if not file_transer:
            return response

        content, file_size = response

        try:
            with open(filename, "wb") as file:

                file.write(content)

                read_bytes = len(content)

                while read_bytes < file_size:
                    chunk = self.client_socket.recv(
                        min(file_size - read_bytes, utils.BUFFER_SIZE)
                    )
                    if chunk == b"":
                        raise RuntimeError("socket connection broken")
                    file.write(chunk)
                    read_bytes += len(chunk)

                return "File sucessfully transfered!"
        except Exception as error:
            return str(error)

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

    def request_message(self, cmd, param, file_size=0):

        return (
            f"{cmd} {param}{utils.SEPARATOR}"
            f"ClientName {self.name}{utils.SEPARATOR}"
            f"FileSize {file_size}{utils.SEPARATOR}{utils.SEPARATOR}"
        )

    def parse_message(self, message):
        message = message.split(
            bytes(utils.SEPARATOR + utils.SEPARATOR, "utf-8")
        )

        header = message[0].decode("utf-8")
        content = message[1]

        header = header.split(utils.SEPARATOR)

        success_code = header[0]
        return_type = header[1].split(" ")[1]
        file_size = header[2].split(" ")[1]

        if success_code == "1":
            # success message
            if return_type == utils.PROMPT_MESSAGE:
                return False, content.decode("utf-8")
            elif return_type == utils.LIST_MESSAGE:
                list_values = ast.literal_eval(content.decode("utf-8"))
                return False, "\n".join(list_values)
            else:
                return True, (content, int(file_size))
        else:
            # error message
            return False, content.decode("utf-8")


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

    ftp_client.connect()

    while cmd != "quit":

        if cmd == "put":
            file_size = os.path.getsize(param)
            message = ftp_client.request_message(
                cmd, param, file_size
            )
            ftp_client.put_to_server(message, param)
        else:
            message = ftp_client.request_message(cmd, param)
            ftp_client.send_to_server(bytes=bytes(message, "utf-8"))

        server_response = ftp_client.recieve_from_server(param)

        # Outputs message on screen.
        print(server_response)

        command = input("myftp>")
        cmd, param = ftp_client.parse_command(command=command)

    message = ftp_client.request_message(cmd, param)
    ftp_client.send_to_server(bytes=bytes(message, "utf-8"))
    ftp_client.terminate()

    print("Bye!")
