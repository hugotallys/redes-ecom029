import socket

if __name__ == "__main__":

    server_name = "localhost"
    server_port = 12000

    # cria o socket cliente especificando a família (AF_INET ipv4)
    # e explicitando que é um socket TCP (SOCK_STREAM)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # conecta ao servidor (apresentação de 3 vias)
    client_socket.connect((server_name, server_port))

    sentence = input("Input lowercase sentence:")

    # envia a cadeia sentence pelo socket do cliente e para a conexao TCP
    client_socket.send(bytes(sentence, "utf-8"))

    # recebe a cadeia enviada pelo servidor
    modified_sentence = client_socket.recv(2048)

    # exibe a mensagem na tela
    print("From server:", modified_sentence.decode("utf-8"))

    # Encerra a conexão com o servidor
    client_socket.close()
