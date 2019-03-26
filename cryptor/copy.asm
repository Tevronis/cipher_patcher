use32

;======================== COPY CODE to original
mov ebx, 4264447
mov edx, 4198911
mov ecx, 511

copy_loop:

mov al, [ebx]
mov [edx], al

cmp ecx, 0
jz end_copy_loop

dec ebx
dec edx
dec ecx
jmp copy_loop

end_copy_loop:

;======================== XOR 1 section
mov ebx, 4209923
mov ecx, 11523

xor_loop:
mov al, byte [ebx]
xor al, 1
mov byte [ebx], al

cmp ecx, 0
jz stop_loop

dec ebx
dec ecx
jmp xor_loop

stop_loop:

;========================== GO OEP

push 4199136
ret
