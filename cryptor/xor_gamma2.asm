use32

;======================== COPY CODE to original
mov ebx, {{ copy_from+copy_len-1 }}
mov edx, {{ copy_to+copy_len-1 }}
mov ecx, {{ copy_len-1 }}

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
x0    db     	7
x1 	  db 		7Bh
m     db     	255
tmp   db 		0

mov ebx, {{ copy_to+xor_len-1 }}
mov ecx, {{ xor_len-1 }}

xor_loop:
    ; GEN
    xor 	eax, eax
	mov     al, [x1]
	mov     [tmp], al
	mov     dl, [x0]
	mov     al, [x1]
	add     eax, edx
	cdq
	idiv    [m]
	mov     [x1], dl
	mov     al, [tmp]
	mov     [x0], al

	mov dl, [x1]
	mov ah,2
    int 21h
    ; /GEN
    mov al, byte [ebx]
    xor al, [x1]
    mov byte [ebx], al

    cmp ecx, 0
    jz stop_loop

    dec ebx
    dec ecx
jmp xor_loop

stop_loop:

;========================== GO OEP

push {{ original_eop }}
ret
