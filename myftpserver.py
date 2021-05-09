import socket

import netifaces


class FTPServer:

    def __init__(self, port_number):

        self.port_number = port_number
        self.ip_address = self.default_route_ip()

    def run(self):
        # Creates TCP Socket.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binds the port number to its socket.
        server_socket.bind(("", self.port_number))

        # Listens until a client "hits" the door.
        server_socket.listen(1)  # Maximum of 1 connection in the queue (review this argument)

        print(f"Server is running on {self.ip_address}:{self.port_number}")

        while True:
            # Creates the client connection socket
            connection_socket, addr = server_socket.accept()

            # Recieves the message sent by the client.
            sentence = connection_socket.recv(2048)
            captilized_sentence = sentence.upper()

            # Sends the message back to the client, but captilzed.
            connection_socket.send(captilized_sentence)
            connection_socket.close()

    def default_route_ip(self):
        """
        Returns the first ip address on the interface
        associated with the default route.
        """
        # Name of the default interface.
        iface = netifaces.gateways()["default"][netifaces.AF_INET][1]
        return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["addr"]


if __name__ == "__main__":

    ftp_server = FTPServer(port_number=12000)
    ftp_server.run()
