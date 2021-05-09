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

contador = [0,0]
while True:
    while (contador[0] < 3) and (contador[1] < 3):
        j_cliente = clientSocket.recv(2048).decode()
        print(f'Usted jugó {j_cliente}.')

        cachipunSocket.sendto('GETSHAPE'.encode(), cachipunAddr)
        j_cachipun = cachipunSocket.recv(2048)
        print(f'El servidor cachipun jugó {j_cachipun}.')

        if (utilities.beats[(j_cliente, j_cachipun)] == utilities.WIN):
            contador[0] += 1

        elif (utilities.beats[(j_cliente, j_cachipun)] == utilities.LOSE):
            contador[1] += 1
        
        elif (utilities.beats[(j_cliente, j_cachipun)] != utilities.DRAW):
            raise Exception()

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
