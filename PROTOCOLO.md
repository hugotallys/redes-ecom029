# MyFTP - Cliente e Servidor FTP Simples

# Protocolo proposto

O protocolo da camada de aplicação proposto segue o seguinte formato. Note que a indentação com quebra de linha foi inserida somente por questões visuais:

#### Mensagem de requisição

```
COMMAND PARAMETER<SEPARATOR>
ClientName CLIENT_NAME<SEPARATOR>
FileSize FILESIZE<SEPARATOR>
<SEPARATOR>
CONTENT
```

#### Mensagem de resposta

```
STATUS_CODE<SEPARATOR>
ReturnType RETURN_TYPE<SEPARATOR>
FileSize FILE_SIZE<SEPARATOR>
<SEPARATOR>
CONTENT
```

Onde:

* __STATUS_CODE__ vale "0" se a requisição falhou e "1" se foi sucedida.
* __RETURN_TYPE__ indica o tipo de mensagem sendo enviada. Pode ser:
    * "PromptMessage", "ListMessage" ou "FileMessage"
* __FILE_SIZE__ é o tamanho do arquivo sendo enviado pelo servidor.
* __CONTENT__ é o conteúdo enviado.