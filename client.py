import socket
import utilities

s = socket.socket(type = utilities.TCP)
s.connect(('localhost', 50366))

print('Solicitando el inicio de una partida...')
s.send('REQUESTGAME'.encode())
response = s.recv(2048).decode()

if response == 'NO':
    s.close()
    exit('Solicitud denegada, finalizando ejecución...')
elif response != 'OK':
    raise Exception() # Error
print('Solicitud aceptada')

print('Solicitando fin de la partida...')
s.send('STOP'.encode())
response = s.recv(2048).decode()

if response != 'OK':
    raise Exception() # Error
print('Solicitud aceptada, finalizando ejecución...')
s.close()