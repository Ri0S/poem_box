from socket import *
import generate
import TTS

s = socket(AF_INET, SOCK_STREAM)
port = 33890
s.bind(('', port))

s.listen(100)
c = None

generate.setup(5, 'random_half_less10_up5_newline_replaced.txt', 'kernel5_random_half_less10_up5_newline_replaced_0.pkl')
print('ready')

while True:
    sock, addr = s.accept()
    print('accept')
    seed = sock.recv(1024).decode('utf-8').strip()

    generate.gen(seed)
    if TTS.T2M('./sample/sample.txt'):
        with open('./sample/sample.mp3', 'rb') as f:
            sock.sendall(f.read())

        sock.sendall('---$---'.encode('utf-8'))

        with open('./sample/sample.txt', 'rb') as f:
            sock.sendall(f.read())
    sock.close()


# import socket
#
# s = socket.socket()
# host = 'xxx.xxx.xxx.xxx'
# port = 33890
#
# seed = '안녕'
#
# s.connect((host, port))
# f = open('sample.mp3', 'wb')
# s.send(seed.encode('utf-8'))
#
# while True:
#     a = s.recv(1024)
#     if a == b'':
#         break
#
#     if '---$---'.encode('utf-8') in a:
#         a = a.split('---$---'.encode('utf-8'))
#         f.write(a[0])
#         f.close()
#         f = open('sample.txt', 'wb')
#         f.write(a[1])
#     else:
#         f.write(a)
