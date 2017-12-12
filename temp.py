with open('./data/random_file_less10_up5_newline_blank_replaced_drop.txt', 'rb') as f:
    for i, a in enumerate(f):
        continue
f2 = open('./data/random_half_file_less10_up5_newline_blank_replaced_drop.txt', 'wb')
with open('./data/random_file_less10_up5_newline_blank_replaced_drop.txt', 'rb') as f:
    for idx, a in enumerate(f):
        f2.write(a)
        if idx > i/2:
            break