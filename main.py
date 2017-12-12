import socket
import generate
import TTS

s = socket.socket()
host = socket.gethostname()
port = 12345
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

s.listen(5)
c = None

while True:
    c, addr = s.accept()
    print( 'Got connection from', addr)

    seed = c.recv(1024).decode('utf-8').strip()

    generate(seed)
    if TTS.T2M('./sample/sample.txt'):
        f = open('./sample/sample.mp3')
        c.send(f.read())