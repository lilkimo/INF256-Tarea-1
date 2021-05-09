from socket import socket
import utilities

class Client:
    gameOn = False 
    def __init__(self, addr):
        self.s = socket(type = utilities.TCP)
        self.s.connect(addr)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if not self.finish():
            print('Se ha finalizado la ejecución del cliente durante una partida, esto podría ocacionar que los servidores no se cierren.')
            self.s.close()
        print('')

    def requestGame(self) -> bool:
        print('Solicitando el inicio de una partida...')
        self.s.send('REQUESTGAME'.encode())
        response = self.s.recv(2048).decode()
        if response == 'NO':
            print('Solicitud rechazada')
            return False
        elif response != 'OK':
            raise Exception()
        
        self.gameOn = True
        print('Solicitud aceptada')
        return True
    
    def play(self, shape: str) -> int:
        if not self.gameOn:
            raise Exception()
        if shape not in utilities.shapes:
            raise Exception()
        print(shape)
        '''
        self.s.send(shape.encode())
        response = self.s.recv(2048).decode()

        if response not in utilities.results:
            raise Exception()
        return response
        '''
    
    def finish(self) -> bool:
        print('Solicitando fin de la partida...')
        if self.gameOn:
            print('No se pudo finalizar la partida porque aún no hay un ganador')
            return False

        self.s.send('STOP'.encode())
        response = self.s.recv(2048).decode()

        if response != 'OK':
            raise Exception()
        print('Solicitud aceptada, finalizando ejecución...')
        self.s.close()
        return True

def main():
    with Client(('localhost', 50366)) as client:
        if client.requestGame():
            jugada = input('Ingrese su jugada: ')
            while jugada.upper().strip() not in utilities.shapesES:
                jugada = input(f'{jugada} no es una jugada válida.\nIngrese su jugada: ')
            client.play(utilities.shapesES[jugada.upper().strip()])

if __name__ == '__main__':
    main()