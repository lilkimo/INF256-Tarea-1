import socket

def connectToCachipunServer():
    addr = 'localhost'
    port = 50001

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto('ISAVAILABLE?'.encode(), (addr, port))

    response = s.recv(2048)
    return (response, s)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50366)) #Al poner el puerto 0 el SO busca automáticamente un socket desocupado.

s.listen(1)
print(f'Servidor TCP escuchando en: {s.getsockname()[1]}')

clientSocket, clientAddr = s.accept()
response = clientSocket.recv(2048).decode()
if response != 'REQUESTGAME':
    # Error
    pass

response, _ = connectToCachipunServer()
clientSocket.send(response)
_.close()
