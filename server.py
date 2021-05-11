from socket import socket
import utilities

class Server:
    def __init__(self, addr, cachipunAddr):
        self.cachipunA = cachipunAddr
        self.cachipunS = socket(type = utilities.UDP)
        self.s = socket(type = utilities.TCP)
        self.s.bind(addr)
        self.s.listen(1)
        print(f'Servidor TCP escuchando en: {self.s.getsockname()[1]}')
        self.clientS, _ = self.s.accept()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.s.close()
        self.cachipunS.close()
        self.clientS.close()
    
    def hearClient(self, buffer: int = 2048) -> bytes:
        return self.clientS.recv(buffer)
    
    def hearCachipun(self, msg: bytes, buffer: int = 2048) -> bytes:
        self.cachipunS.sendto(msg, self.cachipunA)
        return self.cachipunS.recv(buffer)
    
    def game(self) -> bool:
        clientCount = 0
        cachipunCount = 0
        while clientCount < 3 and cachipunCount < 3:
            shapes = (self.hearClient().decode(), self.hearCachipun('GETSHAPE'.encode()).decode())
            if utilities.beats[shapes] == utilities.WIN:
                result = 'WIN'
                clientCount += 1
            elif (utilities.beats[shapes] == utilities.LOSE):
                result = 'LOSE'
                cachipunCount += 1
            elif (utilities.beats[shapes] != utilities.DRAW):
                raise Exception()
            else:
                result = 'DRAW'

            if clientCount == 3:
                self.clientS.send(f'{result},WIN'.encode())
                return True
            elif cachipunCount == 3:
                self.clientS.send(f'{result},LOSE'.encode())
                return False
            elif clientCount > 3 or cachipunCount > 3:
                raise Exception()
            self.clientS.send(f'{result},CONTINUE'.encode())

def main():
    with Server(('localhost', 50366), ('localhost', 50004)) as server:
        response = server.hearClient()
        print(f'Solicitud {response.decode()} recibida.')
        if response.decode() != 'REQUESTGAME':
            raise Exception()
        response = server.hearCachipun(response)
        print(f'Respuesta {response.decode()} recibida.')

        while True:
            server.clientS.send(response)
            if response.decode() == 'OK':
                server.game()
            response = server.hearClient()
            print(f'Solicitud {response.decode()} recibida.')
            if response.decode() == 'REQUESTGAME':
                response = server.hearCachipun(response)
            elif response.decode() == 'STOP':
                response = server.hearCachipun(response)
                if response.decode() != 'OK':
                    raise Exception()
                server.clientS.send(response)
                print('Finalizando ejecución...')
                break

if __name__ == '__main__':
    main()
'''
cachipunAddr = ('localhost', 50001)
cachipunSocket = socket(type = utilities.UDP)

s = socket(type = utilities.TCP)
s.bind(('localhost', 50366)) #Al poner el puerto 0 el SO busca automáticamente un socket desocupado.
s.listen(1)
#print(f'Servidor TCP escuchando en: {s.getsockname()[1]}')
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
        j_cachipun = cachipunSocket.recv(2048).decode()
        print(f'El servidor cachipun jugó {j_cachipun}.')

        if (utilities.beats[(j_cliente, j_cachipun)] == utilities.WIN):
            contador[0] += 1
            if contador[0] >= 3:
                clientSocket.send('WIN'.encode())
                break
        elif (utilities.beats[(j_cliente, j_cachipun)] == utilities.LOSE):
            contador[1] += 1
            if contador[1] >= 3:
                clientSocket.send('LOSE'.encode())
                break
        elif (utilities.beats[(j_cliente, j_cachipun)] != utilities.DRAW):
            raise Exception()
        
        print(contador)
        clientSocket.send('CONTINUE'.encode())

    response = clientSocket.recv(2048).decode()
    print(f'Solicitud {response} recibida.')
    if response == 'REQUESTGAME':
        cachipunSocket.sendto('ISAVAILABLE?'.encode(), cachipunAddr)
        response = cachipunSocket.recv(2048)
        print('Respuesta del servidor cachipun recibida.')
        clientSocket.send(response)
        print('Respuesta reenviada al cliente.')
        contador = [0,0]
    elif response == 'STOP':
        cachipunSocket.sendto(response.encode(), cachipunAddr)
        print('Solicitud reenviada al servidor cachipun.')
        response = cachipunSocket.recv(2048)
        if response.decode() != 'OK':
            raise Exception() # Error
        clientSocket.send(response)
        print('Respuesta reenviada al cliente.')
        break
print('Finalizando ejecución...')
cachipunSocket.close()
'''
