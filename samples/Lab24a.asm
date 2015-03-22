
8000:
    MVI A, B0
    OUT 83
    MVI A, 0E
    SIM
    EI

LOOP:   JMP LOOP

8FB3: JMP 9000

9000:   IN 80
        OUT 81
        EI
        RET
