section .data
    msg db "Hello, World!", 0xA  ; Message avec saut de ligne
    len equ $ - msg               ; Taille du message

section .text
    global _start                 ; Point d'entrée

_start:
    mov rax, 1      ; syscall write (1)
    mov rdi, 1      ; File descriptor (stdout)
    mov rsi, msg    ; Adresse du message
    mov rdx, len    ; Taille du message
    syscall         ; Appel système

    mov rax, 60     ; syscall exit (60)
    xor rdi, rdi    ; Code de retour 0
    syscall         ; Quitter le programme
