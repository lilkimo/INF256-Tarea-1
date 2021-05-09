from socket import SOCK_DGRAM, SOCK_STREAM

TCP = SOCK_STREAM
UDP = SOCK_DGRAM

shapes = [
    'ROCK',
    'PAPER',
    'SCISSORS'
]

shapesES = {
    'PIEDRA': 'ROCK',
    'PAPEL': 'PAPER',
    'TIJERAS': 'SCISSORS'
}

WIN = 0
LOSE = 1
DRAW = 2
results = [WIN, LOSE, DRAW]

# 0: WIN jugador 1, 1: LOSE jugador 1, 2: DRAW
beats = {
    ('ROCK', 'ROCK'): DRAW,
    ('ROCK', 'PAPER'): LOSE,
    ('ROCK', 'SCISSORS'): WIN,

    ('PAPER', 'ROCK'): WIN,
    ('PAPER', 'PAPER'): DRAW,
    ('PAPER', 'SCISSORS'): LOSE,

    ('SCISSORS', 'ROCK'): LOSE,
    ('SCISSORS', 'PAPER'): WIN,
    ('SCISSORS', 'ROCK'): DRAW
}