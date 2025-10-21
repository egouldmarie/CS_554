.text
.globl generated_function
generated_function:
    # Function prologue
    addi sp, sp, -16
    sd ra, 8(sp)
    sd fp, 0(sp)
    addi fp, sp, 16
    # Variable array pointer in a1

    li x8, 0
    mv x9, x8
    li x10, 1
    mv x11, x10
    li x12, 0
    mv x13, x12
label_1:

    sub x15, x14, x13
    seqz x15, x15
    seqz a0, x15
    beqz a0, label_2

    add a0, x9, x11
    sd a0, 32(a1)
    mv x9, x11
    ld a0, 32(a1)
    mv x11, a0
    li a0, 1
    sub a0, x14, a0
    mv x14, a0
    li a0, 0
    mv x13, a0
    j label_1
label_2:

    sd x9, 24(a1)
    # Function epilogue
    ld ra, 8(sp)
    ld fp, 0(sp)
    addi sp, sp, 16
    ret
