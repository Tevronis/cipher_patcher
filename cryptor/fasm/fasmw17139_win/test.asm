use32
	x0    db     	7
	x1 	  db 		7Bh
	m     db     	99h
	n     db 		0Ah
	i     db     	0
	tmp   db 		0
	aD    db 		'%d',0Ah,0
	loop1:
		xor 	eax, eax
		mov     al, [i]
		cmp     al, [n]
		jge     short exit
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
		mov     al, [x1]
		mov     [esp+4], eax
		;mov     [esp], [aD]
		;call    _printf
		add     [i], 1
		jmp     short loop1
	exit:
		mov     eax, 0