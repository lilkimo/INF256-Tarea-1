import socket
import utilities

cachipunAddr = ('localhost', 50001)
cachipunSocket = socket.socket(type = utilities.UDP)

s = socket.socket(type = utilities.TCP)
s.bind(('localhost', 50366)) #Al poner el puerto 0 el SO busca automáticamente un socket desocupado.
s.listen(1)
print(f'Servidor TCP escuchando en: {s.getsockname()[1]}')
clientSocket, clientAddr = s.accept()

response = clientSocket.recv(2048).decode()
print(f'Solicitud {response} recibida.')
if response != 'REQUESTGAME':
    raise Exception()

cachipunSocket.sendto('ISAVAILABLE?'.encode(), cachipunAddr)
response = cachipunSocket.recv(2048)
print('Respuesta del servidor cachipun recibida.')
clientSocket.send(response)
print('Respuesta reenviada al cliente.')

while True:
    # Jugadas
    # código
    # código
    # código
    # código

    response = clientSocket.recv(2048).decode()
    print(f'Solicitud {response} recibida.')
    if response == 'REQUESTGAME':
        cachipunSocket.sendto('ISAVAILABLE?'.encode(), cachipunAddr)
        response = cachipunSocket.recv(2048)
        print('Respuesta del servidor cachipun recibida.')
        clientSocket.send(response)
        print('Respuesta reenviada al cliente.')
    elif response == 'STOP':
        cachipunSocket.sendto(response.encode(), cachipunAddr)
        print('Solicitud reenviada al servidor cachipun.')
        response = cachipunSocket.recv(2048)
        if response.decode() != 'OK':
            raise Exception() # Error
        clientSocket.send(response)
        print('Respuesta reenviada al cliente.')
        break
print('Finalizando ejecución')
cachipunSocket.close()
