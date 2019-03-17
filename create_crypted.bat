g++ sample/main.cpp -o prog.exe
REM script.py <filename> <func_addr> <func_size> <xor_key>
python cryptor/script.py prog.exe 894 58 9
copy prog.exe C:\cygwin\home\Mike
copy crypted.exe C:\cygwin\home\Mike
