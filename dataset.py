import os
import random

dir_list = os.listdir('./poem/')
random_poem = []

print(dir_list)

whole_file = open('./data/random_file_less10_up5_newline_replaced.txt', 'wb')

for directory in dir_list:
    file_list = os.listdir('./poem/' + directory + '/')
    if len(file_list) < 5:
        continue
    for file in file_list:
        with open('./poem/' + directory + '/' + file, 'rb') as f:
            random_poem.append('./poem/' + directory + '/' + file)

random.shuffle(random_poem)

length = len(random_poem)
for i, file in enumerate(random_poem):
    # if i > length/2:
    #     break
    with open(file, 'rb') as f:
        f.readline()
        while True:
            if f.readline() != '\r\n'.encode('utf-8'):
                break
        while True:
            if f.readline() != '\r\n'.encode('utf-8'):
                break

        for line in f:
            temp = line.decode('utf-8').split()
            if len(temp) < 10 and line != '\r\n'.encode('utf-8'):
                for tt in temp:
                    whole_file.write(tt.encode('utf-8') + ' '.encode('utf-8'))
                whole_file.write('+++$+++ '.encode('utf-8'))
        whole_file.write('\r\n'.encode('utf-8'))

# for directory in dir_list:
#     file_list = os.listdir('./poem/' + directory + '/')
#     if len(file_list) < 5:
#         continue
#     for file in file_list:
#         with open('./poem/' + directory + '/' + file, 'rb') as f:
#             f.readline()
#             for line in f:
#                 if len(line.decode('utf-8').split()) < 10 and line != '\r\n'.encode('utf-8'):
#                     whole_file.write(line)
#             whole_file.write('+++$+++\r\n'.encode('utf-8'))
#
