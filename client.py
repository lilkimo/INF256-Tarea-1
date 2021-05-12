from socket import socket
import utilities

class Client:
    # Esta variable indica si estamos en partida o no.
    gameOn = False 
    def __init__(self, addr):
        # Creo el socket y me conecto con el servidor intermedio
        self.s = socket(type = utilities.TCP)
        self.s.connect(addr)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if not self.finish():
            print('Se ha finalizado la ejecución del cliente durante una partida, esto podría ocasionar que los servidores no se cierren.')
            self.s.close()
        print('')

    def requestGame(self) -> bool:
        # Aquí solicito el inicio de una partida
        print('Solicitando el inicio de una partida...')
        self.s.send('REQUESTGAME'.encode())
        response = self.s.recv(2048).decode()
        if response == 'NO':
            print('Solicitud rechazada')
            return False
        elif response != 'OK':
            raise Exception()
        
        # Si la solicitud es aceptada entonces estamos en partida.
        self.gameOn = True
        print('Solicitud aceptada\n---')
        return True
    
    def play(self, shape: str) -> str:
        # Si no estamos en partida o se usa un movimiento que no existe hay que arrojar un error.
        if not self.gameOn:
            raise Exception()
        if shape not in utilities.shapes:
            raise Exception()
        
        # Envío la jugada
        self.s.send(shape.encode())
        # Recibo el resultado, las victorias, derrotas, lo que jugó el servidor cachipun y si se debe continuar el juego o la pardia se ganó o perdió.
        result, victories, loses, bot, toDo = self.s.recv(2048).decode().split(',')
        if toDo in ('WIN', 'LOSE'):
            # Si gané o perdí la partida entonces ya se terminó esta.
            self.gameOn = False
        elif toDo != 'CONTINUE':
            raise Exception()

        print(f'El bot jugó {utilities.shapesEN[bot]}')

        if result == 'WIN':
            print('Ganaste esta ronda')
        elif result == 'LOSE':
            print('Perdiste esta ronda')
        elif result == 'DRAW':
            print('Empataron')
        else:
            raise Exception()
        print(f'Ganadas: {victories}|Perdidas: {loses}\n---')
        return toDo
    
    def finish(self) -> bool:
        print('Solicitando fin del juego...')
        # Si la partida aún no ha terminado no se puede finalizar el programa.
        if self.gameOn:
            print('No se pudo finalizar el juego porque aún no hay un ganador')
            return False

        self.s.send('STOP'.encode())
        response = self.s.recv(2048).decode()

        if response != 'OK':
            raise Exception()
        print('Solicitud aceptada, finalizando ejecución...')
        self.s.close()
        return True

def main():
    with Client(('localhost', 49152)) as client:
        # Loop opcional
        while True:
            # Aquí solicitamos la partida
            if client.requestGame():
                result = 'CONTINUE'
                # Siempre que haya finalizado la partida se debe seguír pidiendo jugadas
                while result == 'CONTINUE':
                    jugada = input('Ingrese su jugada: ')
                    # Aquí pedimos movimientos hasta que se ingrese uno válido (Piedra, Papel o Tijeras)
                    while jugada.upper().strip() not in utilities.shapesES:
                        jugada = input(f'{jugada} no es una jugada válida.\nIngrese su jugada: ')
                    result = client.play(utilities.shapesES[jugada.upper().strip()])
                if result == 'WIN':
                    print('¡Has ganado la partida!')
                else:
                    print('Has perdido la partida...')
            while True:
                newMatch = input('¿Desea comenzar una nueva partida? (S/N): ')
                # Aquí se pide S/N hasta que se ingrese una opción válida
                if newMatch.upper().strip() not in ('S', 'N'):
                    print(f'{newMatch} no es una opción válida')
                else:
                    break
            if newMatch.upper().strip() == 'N':
                break

if __name__ == '__main__':
    main()