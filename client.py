import socket
import utilities

def finish(thisS: socket.socket):
    print('Solicitando fin de la partida...')
    thisS.send('STOP'.encode())
    response = thisS.recv(2048).decode()

    if response != 'OK':
        raise Exception() # Error
    print('Solicitud aceptada, finalizando ejecución...')
    thisS.close()

s = socket.socket(type = utilities.TCP)
s.connect(('localhost', 50366))

print('Solicitando el inicio de una partida...')
s.send('REQUESTGAME'.encode())
response = s.recv(2048).decode()

if response == 'NO':
    finish(s)
elif response != 'OK':
    raise Exception() # Error
print('Solicitud aceptada')

finish(s)