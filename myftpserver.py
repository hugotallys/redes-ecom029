import os
import sys
import socket
import utils


class FileManager:

    def __init__(self):

        self.sessions = None
        self.remote_path = "myftp"

        if not os.path.exists(self.remote_path):
            os.mkdir(self.remote_path)

    def register_session(self, client_name):
        """
        Associates client_name to a working path.
        """
        if self.sessions is not None:
            if client_name not in self.sessions:
                self.sessions[client_name] = self.remote_path
        else:
            self.sessions = {client_name: self.remote_path}

    def unregister_session(self, client_name):
        """
        Removes the associated path of client_name.
        """
        if client_name in self.sessions:
            del self.sessions[client_name]

    def pwd(self, client_name):
        """
        Outputs the current working directory on client screen.
        """
        return self.format_message(
            status_code=utils.SUCCESS, return_type=utils.PROMPT_MESSAGE,
            content=self.sessions[client_name]
        )

    def mkdir(self, client_name, dirname):
        dir_path = os.path.join(self.sessions[client_name], dirname)

        try:
            os.mkdir(dir_path)
            return self.format_message(
                status_code=utils.SUCCESS, return_type=utils.PROMPT_MESSAGE,
                content=f"Direcotry created at {dir_path}"
            )
        except Exception as error:
            return self.format_message(
                status_code=utils.ERROR, return_type=utils.PROMPT_MESSAGE,
                content=str(error)
            )

    def cd(self, client_name, dirname):

        if dirname == "..":
            self.sessions[client_name] = os.path.split(
                self.sessions[client_name]
            )[0]

            return self.format_message(
                status_code=utils.SUCCESS, return_type=utils.PROMPT_MESSAGE,
                content=f"Current remote path is {self.sessions[client_name]}"
            )

        dir_list = [
            filename for filename in os.listdir(self.sessions[client_name])
            if os.path.isdir(
                os.path.join(self.sessions[client_name], filename)
            )
        ]

        if dirname not in dir_list:
            return self.format_message(
                status_code=utils.ERROR, return_type=utils.PROMPT_MESSAGE,
                content=f"{dirname} not found in the current remote path."
            )

        self.sessions[client_name] = os.path.join(
            self.sessions[client_name], dirname
        )

        return self.format_message(
            status_code=utils.SUCCESS, return_type=utils.PROMPT_MESSAGE,
            content=f"Current remote path is {self.sessions[client_name]}"
        )

    def ls(self, client_name):
        file_list = [
            filename for filename in os.listdir(self.sessions[client_name])
        ]
        return self.format_message(
            status_code=utils.SUCCESS, return_type=utils.LIST_MESSAGE,
            content=str(file_list)
        )

    def delete(self, client_name, filename):
        filepath = os.path.join(self.sessions[client_name], filename)

        try:
            os.remove(filepath)
            return self.format_message(
                status_code=utils.SUCCESS, return_type=utils.PROMPT_MESSAGE,
                content=f"Deleted file {filepath}"
            )
        except Exception as error:
            return self.format_message(
                status_code=utils.SUCCESS, return_type=utils.PROMPT_MESSAGE,
                content=str(error)
            )

    def put(self, client_name, filename, filesize, content, socket):

        filepath = os.path.join(
            self.sessions[client_name], filename
        )

        with open(filepath, "wb") as file:

            file.write(content)

            read_bytes = len(content)

            while read_bytes < int(filesize):
                chunk = socket.recv(
                    min(int(filesize) - read_bytes, utils.BUFFER_SIZE)
                )
                if chunk == b'':
                    raise RuntimeError("socket connection broken")
                file.write(chunk)
                read_bytes += len(chunk)

        return self.format_message(
            status_code=utils.SUCCESS, return_type=utils.PROMPT_MESSAGE,
            content="File sucessfully transfered!"
        )

    def format_message(self, status_code, return_type, content=""):
        return (
            f"{status_code}{utils.SEPARATOR}"
            f"ReturnType {return_type}{utils.SEPARATOR}{utils.SEPARATOR}"
            f"{content}"
        )


class FTPServer:

    def __init__(self, port_number):

        self.port_number = port_number
        self.name = utils.default_route_ip()

    def parse_message(self, message):
        """
        Recieves the formated message and parses each componenet.
        :param message: String representing the client request.
        """
        message = message.split(utils.SEPARATOR)

        command = message[0].split(" ")[0]
        parameter = message[0].split(" ")[1]
        client_name = message[1].split(" ")[1]
        file_size = message[2].split(" ")[1]

        return client_name, command, parameter, file_size

    def run(self):

        file_manager = FileManager()

        # Creates TCP Socket.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binds the port number to its socket.
        server_socket.bind(("", self.port_number))

        # Listens until a client "hits" the door.
        server_socket.listen(1)  # Maximum of 1 connection in the queue

        print(f"Server is running on {self.name}:{self.port_number}")

        while True:
            # Creates the client connection socket
            connection_socket, addr = server_socket.accept()

            # Recieves the message sent by the client.
            message = connection_socket.recv(utils.BUFFER_SIZE)

            message = message.split(
                bytes(utils.SEPARATOR + utils.SEPARATOR, "utf-8")
            )

            header = message[0].decode("utf-8")

            content = message[1]

            client_name, cmd, param, file_size = self.parse_message(header)

            print(header)

            if cmd == "quit":
                file_manager.unregister_session(client_name)
                connection_socket.close()
                continue

            # Registers the client in the file manager.
            file_manager.register_session(client_name=client_name)

            # Executes the command.
            # If the command is not implemented returns error.
            if hasattr(file_manager, cmd):
                if param != "":
                    if cmd == "put":
                        response_message = getattr(file_manager, cmd)(
                            client_name, param, file_size,
                            content, connection_socket
                        )
                    else:
                        response_message = getattr(file_manager, cmd)(
                            client_name, param
                        )
                else:
                    response_message = getattr(file_manager, cmd)(client_name)
            else:
                response_message = f"The command {cmd} is not implemented!"

            connection_socket.send(bytes(response_message, "utf-8"))


if __name__ == "__main__":

    try:
        port_number = sys.argv[1]
    except IndexError:
        raise IndexError(
            (
                "Parameter <port_number> is missing. "
                "To execute this program run:\n"
                "$ python myftpserver.py <port_number>"
            )
        )

    ftp_server = FTPServer(port_number=int(port_number))
    ftp_server.run()
