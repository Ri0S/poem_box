import socket
import sys

s = socket.socket()
host = '14.45.1.234'
port = 33890

if len(sys.argv) < 2:
    seed = ''
else:
    seed = sys.argv[1]


s.connect((host, port))
f = open('sample.mp3', 'wb')
#s.send(seed.encode('utf-8'))
s.send(seed)

while True:
    a = s.recv(1024)

    if a == b'':
        break

    if '---$---'.encode('utf-8') in a:
        a = a.split('---$---'.encode('utf-8'))
        f.write(a[0])
        f.close()
        f = open('sample.txt', 'wb')
        f.write(a[1])
    else:
        f.write(a)
