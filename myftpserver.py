import socket

if __name__ == "__main__":
    server_port = 12000

    # cria o socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # associa o numero da porta do servidor ao seu socket
    server_socket.bind(("", server_port))

    # server_socket é o socket de entrada
    # ficamos "escutando" até que algum cliente bata

    server_socket.listen(1)  # no máximo 1 conexão em fila

    print("Server is listening")

    while 1:
        # cria o scoket de conexão dedicado ao cliente
        connection_socket, addr = server_socket.accept()
        # recebe a mensagem enviada pelo cliente
        sentence = connection_socket.recv(2048)
        captilized_sentence = sentence.upper()
        # manda a mensagem de volta para o cliente
        connection_socket.send(captilized_sentence)
        connection_socket.close()
