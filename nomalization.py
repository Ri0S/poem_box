f = open('./data/random_file_less10_up5_newline_replaced.txt', 'rb')
f2 = open('./data/random_file_less10_up5_newline_replaced_drop.txt', 'wb')

for a in f:
    c = a.decode('utf-8')
    c = c.split()
    if len(c) < 20:
        continue

    tf = False
    for b in c:
        if b != '+++$+++':
            tf = True
            break

    if tf:
        f2.write(a)
#
# import konlpy
# import re
# tagger = konlpy.tag.Twitter()
# f2 = open('./data/random_file_less10_up5_newline_blank_replaced_drop.txt', 'wb')
# with open('./data/random_file_less10_up5_newline_replaced_drop.txt', 'rb') as f:
#     for i, a in enumerate(f):
#         a = a.decode('utf-8')
#         a = a.replace(' ', '☆')
#         a = tagger.morphs(a)
#         for b in a:
#             f2.write(b.encode('utf-8') + ' '.encode('utf-8'))
#         f2.write('\r\n'.encode('utf-8'))
#
