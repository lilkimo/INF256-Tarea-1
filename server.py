from socket import socket
import utilities

class Server:
    def __init__(self, addr, cachipunAddr):
        # Establezco la dirección que escuchamos como la inmutable del servidor cachipun
        self.cachipunAddr = self.cachipunHearingAddr = cachipunAddr
        # Creo el socket con el cual me voy a comunicar con el servidor cachipun
        self.cachipunS = socket(type = utilities.UDP)
        # Aquí creo que socket por el cual se va a conectar el cliente.
        self.s = socket(type = utilities.TCP)
        self.s.bind(addr)
        self.s.listen(1)
        print(f'Servidor TCP establecido en el puerto: {addr[1]}')
        # Aquí acepto y fijo al cliente.
        self.clientS, clientAddr = self.s.accept()
        print(f'Dirección del cliente: {clientAddr}\nEscuchando al servidor cachipun en la dirección: {cachipunAddr}')
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.s.close()
        self.cachipunS.close()
        self.clientS.close()
    
    def hearClient(self, buffer: int = 2048) -> bytes:
        return self.clientS.recv(buffer)
    
    def hearCachipun(self, msg: bytes, buffer: int = 2048) -> bytes:
        # Enviamos algo al servidor cachipun y vemos qué responde
        self.cachipunS.sendto(msg, self.cachipunHearingAddr)
        return self.cachipunS.recv(buffer)

    def requestGame(self, msg: bytes) -> bytes:
        response, port = self.hearCachipun(msg).decode().split(',')
        if response == 'OK':
            print(f'Se cambió la dirección de escucha del servidor cachipun de {self.cachipunHearingAddr} a {(self.cachipunAddr[0], int(port))}')
            self.cachipunHearingAddr = (self.cachipunAddr[0], int(port))
        elif response != 'NO':
            raise Exception()
        return response.encode()
    
    def game(self):
        clientCount = 0
        cachipunCount = 0
        # Aquí hacemos el ciclo de juego hasta que alguno de los dos jugadores gane 3 partidas
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

            # Si el cliente gana le mandamos el mensaje 'WIN' y las datos
            if clientCount == 3:
                self.clientS.send(f'{result},{clientCount},{cachipunCount},{shapes[1]},WIN'.encode())
                break
            # Si el servidor cachipun gana le mandamos al cliente el mensaje 'LOSE' y las datos
            elif cachipunCount == 3:
                self.clientS.send(f'{result},{clientCount},{cachipunCount},{shapes[1]},LOSE'.encode())
                break
            elif clientCount > 3 or cachipunCount > 3:
                raise Exception('Se han superado las 3 victorias necesarias para ganar la partida')
            # Si aún no hay un ganador mandamos 'CONTINUE' y los datos
            self.clientS.send(f'{result},{clientCount},{cachipunCount},{shapes[1]},CONTINUE'.encode())
        # Una vez finalizada la partida solicitamos que puerto que se abrió para jugarla se cierre
        if self.hearCachipun('CLOSE'.encode()).decode() != 'OK':
            raise Exception()
        print(f'Se cambió la dirección de escucha del servidor cachipun de {self.cachipunHearingAddr} a {self.cachipunAddr}')
        self.cachipunHearingAddr = self.cachipunAddr

def main():
    with Server(('localhost', 49152), ('localhost', 49153)) as server:
        response = server.hearClient()
        print(f'Solicitud {response.decode()} recibida.')
        if response.decode() != 'REQUESTGAME':
            raise Exception()
        # Solicitiamos partida
        response = server.requestGame(response)

        while True:
            server.clientS.send(response)
            # Si se aceptó la partida prodecemos a jugarla
            if response.decode() == 'OK':
                server.game()
            response = server.hearClient()
            print(f'Solicitud {response.decode()} recibida.')
            if response.decode() == 'REQUESTGAME':
                response = server.requestGame(response)
            elif response.decode() == 'STOP':
                # Aquí solicitamos finalizar el programa
                response = server.hearCachipun(response)
                if response.decode() != 'OK':
                    raise Exception()
                server.clientS.send(response)
                print('Finalizando ejecución...')
                break
            else:
                raise Exception()

if __name__ == '__main__':
    main()
