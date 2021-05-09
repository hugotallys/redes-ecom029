import socket


class FTPClient:

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

    def recieve_from_server(self):
        """
        Recieves bytes from the server and through the TCP connection.
        """
        return self.client_socket.recv(2048)#what this number means ?

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


if __name__ == "__main__":

    server_name = "localhost"
    server_port = 12000

    ftp_client = FTPClient(server_port=server_port, server_name=server_name)

    command = input("myftp>")
    cmd, param = ftp_client.parse_command(command=command)

    while cmd != "quit":

        ftp_client.connect()

        ftp_client.send_to_server(bytes=bytes(f"{cmd}#{param}\n", "utf-8"))

        modified_sentence = ftp_client.recieve_from_server()

        # Outputs message on screen.
        print("Recieved from server:", modified_sentence.decode("utf-8"))

        command = input("myftp>")
        cmd, param = ftp_client.parse_command(command=command)

        ftp_client.terminate()

    print("Bye!")
