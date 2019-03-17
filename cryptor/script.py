import sys


if len(sys.argv) == 1:
    filename = input('Enter filename:\n>> ')
    addr = int(input('Enter function address:\n>> '), 16)
    size = int(input('Enter function size:\n>> '))
    key = int(input('Enter xor-key:\n>> '))
else:
    filename = sys.argv[1]
    addr = int(sys.argv[2], 16)
    size = int(sys.argv[3])
    key = int(sys.argv[4])


f = bytearray(open(filename, 'rb').read())

for idx in range(addr, addr + size + 1):
    # print(str(hex(f[idx]))[2:], end=' ')
    f[idx] ^= key
# print()
with open('crypted.exe', 'wb') as out:
    out.write(f)



