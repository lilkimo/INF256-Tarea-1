import socket

addr = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((addr, 50366))
print('Solicitando el inicio de una partida...')
message = 'REQUESTGAME'
s.send(message.encode())
response = s.recv(2048).decode()

if response == 'NO':
    s.close()
    exit('Solicitud denegada, finalizando ejecución...')
elif response != 'OK':
    pass
    # Error

print('Solicitud aceptada')
s.close()