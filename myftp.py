import socket


class FTPClient:

    # Creates the client socket specifying the family (AF_INET ipv4)
    # and making explicit that it is a TCP socket (SOCK_STREAM).
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, server_port, server_name):

        self.server_port = server_port
        self.server_name = server_name

    def connect(self):
        """
        Connects to the server (3-way presentation).
        """
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


if __name__ == "__main__":

    server_name = "localhost"
    server_port = 12000

    ftp_client = FTPClient(server_port=server_port, server_name=server_name)
    ftp_client.connect()

    sentence = input("Input lowercase sentence:")

    ftp_client.send_to_server(bytes=bytes(sentence, "utf-8"))

    modified_sentence = ftp_client.recieve_from_server()

    # Outputs message on screen.
    print("Recieved from server:", modified_sentence.decode("utf-8"))

    ftp_client.terminate()
