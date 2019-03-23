g++ sample/main.cpp -o prog.exe
REM script.py <filename> <func_addr> <func_size> <xor_key> 894 58 
python cryptor/script.py prog.exe 894 58 9
C:\Python27\python.exe cryptor/cryptor.py -x crypted.exe 1
copy prog.exe C:\cygwin\home\Mike
copy crypted.exe C:\cygwin\home\Mike
copy result.exe C:\cygwin\home\Mike
