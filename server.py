from socket import socket
import utilities

class Server:
    def __init__(self, addr, cachipunAddrddr):
        self.cachipunAddr = self.cachipunHearingAddr = cachipunAddrddr
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
        self.cachipunS.sendto(msg, self.cachipunHearingAddr)
        return self.cachipunS.recv(buffer)

    def requestGame(self, msg: bytes) -> bytes:
        response, port = self.hearCachipun(msg).decode().split(',')
        if response == 'OK':
            self.cachipunHearingAddr = (self.cachipunAddr[0], int(port))
        return response.encode()
    
    def game(self):
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
                self.clientS.send(f'{result},{clientCount},{cachipunCount},{shapes[1]},WIN'.encode())
                break
            elif cachipunCount == 3:
                self.clientS.send(f'{result},{clientCount},{cachipunCount},{shapes[1]},LOSE'.encode())
                break
            elif clientCount > 3 or cachipunCount > 3:
                raise Exception()
            self.clientS.send(f'{result},{clientCount},{cachipunCount},{shapes[1]},CONTINUE'.encode())
        if self.hearCachipun('CLOSE'.encode()).decode() != 'OK':
            raise Exception()
        self.cachipunHearingAddr = self.cachipunAddr

def main():
    with Server(('localhost', 49152), ('localhost', 49153)) as server:
        response = server.hearClient()
        print(f'Solicitud {response.decode()} recibida.')
        if response.decode() != 'REQUESTGAME':
            raise Exception()
        response = server.requestGame(response)

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
