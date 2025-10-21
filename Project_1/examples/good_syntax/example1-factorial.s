.text
.globl example1-factorial
example1-factorial:
    # Function prologue
    addi sp, sp, -16
    sd ra, 8(sp)
    sd fp, 0(sp)
    addi fp, sp, 16
    # Variable array pointer in a1

    mv x9, x8
    li x10, 1
    mv x11, x10
label_1:

    li x12, 1
    slt x13, x12, x9
    beqz x13, label_2

    mul x14, x11, x9
    mv x11, x14
    li x15, 1
    sub a0, x9, x15
    mv x9, a0
    j label_1
label_2:

    li a0, 0
    mv x9, a0
    sd x11, 0(a1)
    # Function epilogue
    ld ra, 8(sp)
    ld fp, 0(sp)
    addi sp, sp, 16
    ret
