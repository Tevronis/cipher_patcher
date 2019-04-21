import sys


if len(sys.argv) == 1:
    filename = input('Enter filename:\n>> ')
    key = int(input('Enter xor-key:\n>> '))
else:
    filename = sys.argv[1]
    key = int(sys.argv[4])

f = bytearray(open(filename, 'rb').read())

# Вычисляем сигнатуру, сигнальные биты
pos = 0
for idx in range(len(f)):
	if f[idx] == 0x97 and f[idx + 1] == 0x43 and f[idx + 2]:
		pos = idx

# ищем начало функции
for idx in range(pos, 0, -1):
	if f[idx] == 0x55 and f[idx + 1] == 0x89 and f[idx + 2] == 0xE5:
		start = idx
		break
# ищем конец функции
for idx in range(start+1, len(f)):
	if f[idx] == 0x55 and f[idx + 1] == 0x89 and f[idx + 2] == 0xE5:
		finish = idx
		break
# шифруем
for idx in range(start, finish):
    print(str(hex(f[idx]))[2:], end=' ')
    f[idx] ^= key

with open('crypted.exe', 'wb') as out:
    out.write(f)



