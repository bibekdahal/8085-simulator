   
    MVI A, B4
    OUT 43

    MVI A, FF
    OUT 42
    
    CALL GENERATE
    MVI A, 00
    OUT 42

    MVI A, 0C
    SIM
    EI
LOOP: 
    JMP LOOP

8FB3: 
    JMP BBL

8FB9:
    JMP SSL

BBL:
    CALL BUBBLE_SORT
    MVI A, F0
    OUT 42
    EI
    RET
SSL:
    CALL SELECTION_SORT
    MVI A, 0F
    OUT 42
    EI
    RET


; Get table address offset by A in HL pair
GET_MEMORY:
    LXI H, TABLE
    ADD L
    JNC L123
    INR H
L123:
    MOV L, A
    RET

; Swap data at indices pointed by registers D and E
SWAP:
        PUSH D
        PUSH B
        MOV A, D
        CALL GET_MEMORY
        MOV B, M
        MOV A, E
        CALL GET_MEMORY
        MOV E, M
        MOV M, B
        MOV A, D
        CALL GET_MEMORY
        MOV M, E
        POP B
        POP D
        RET


; Selection sort the table data
SELECTION_SORT:
        MVI C, 0        ; j = 0
Outer0: MOV A, C        ; while j < n-1
        CPI 0x63
        JZ Outer1

        MOV D, C            ; imin = j
        MOV E, C            ; i = j+1
        INR E
Inner0: MOV A, E            ; while i < n
        CPI 0x64
        JZ Inner1
        
        MOV A, E                ; a[i]
        CALL GET_MEMORY
        MOV B, M

        MOV A, D                ; a[imin]
        CALL GET_MEMORY
        MOV A, M

        CMP B                   ; if (a[i] < a[imin])
        JC L456                     ; imin = i
        JZ L456
        MOV D, E

L456:
        INR E                   ; i++
        JMP Inner0          ; end while

Inner1:        
        MOV A, C            ; if imin != j
        CMP D
        JZ L567
        MOV E, C
        CALL SWAP                ; swap(a[i], a[imin]

L567:
        INR C           ; end while
        JMP Outer0
Outer1:
        RET


BUBBLE_SORT:
        MVI C, 0            ; swapped = false
        MVI E, 1            ; for i = 1 to n-1
INR0:   MVI A, 0x64         
        CMP E
        JZ INR1

        MOV D, E                ; if a[i-1] < a[i]
        DCR D
        MOV A, D
        CALL GET_MEMORY
        MOV B, M
        MOV A, E
        CALL GET_MEMORY
        MOV A, M

        CMP B
        JC L678
        JZ L678
        CALL SWAP                   ; swap(a[i-1], a[i])
        MVI C, 1                    ; swapped = true
L678:
        INR E
        JMP INR0

INR1:
        MOV A, C            ; repeat until swapped = false
        CPI 0
        JNZ BUBBLE_SORT
        RET

GENERATE:
    LXI H, TABLE
    MVI C, 0x64
    MVI E, 0x00
    MVI A, 36
    CALL SEED
L1: CALL RANDOM
    MOV B, A
    CALL CHECK_TABLE
    CPI 0x1
    JNZ L1
    
    MOV M, B
    INX H
    INR E
    DCR C
    JNZ L1
    RET

SEED:
        STA X    ; INPUT in A
        RET

RANDOM:          ; OUTPUT in A
        LDA X
        CPI 0
        JZ L098
        MOV B, A
        LDA Y
        INR A
        STA Y
        ADD B
L098:
        RLC
        MOV B, A
        LDA X
        XRA B
        
        STA X
        RET
        
X: 0C
Y: 0

CHECK_TABLE:
    PUSH B
    PUSH H

    LXI H, TABLE
    MOV C, E
L2:
    MOV A, C
    CPI 0
    JZ L4
    MOV A, B
    CMP M
    JNZ L3
    MVI A, 0x0
    POP H
    POP B
    RET
L3: INX H
    DCR C
    JMP L2
L4: MVI A, 0x1
    POP H
    POP B
    RET

TABLE:
