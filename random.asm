
SEED:
        STA X    ; INPUT in A

RANDOM:          ; OUTPUT in A
        LDA X
        RLC
        RLC
        RLC
        MOV B, A
        LDA X
        XRA B
        
        STA X
        

X: 0C

Y:
