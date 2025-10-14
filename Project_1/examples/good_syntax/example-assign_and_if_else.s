.text
.globl generated_function
generated_function:
    # Function prologue
    addi sp, sp, -16
    sd ra, 8(sp)
    sd fp, 0(sp)
    addi fp, sp, 16
    # Variable array pointer in a1

    li x8, 3
    mv x9, x8
    li x10, 0
    sub x11, x9, x10
    seqz x11, x11
    beqz x11, label_1

    li x12, 1
    add x13, x9, x12
    mv x9, x13
    li x14, 2
    mul x15, x14, x9
    li a0, 3
    add a0, x15, a0
    sd a0, 8(a1)
    j label_2
label_1:

    li a0, 0
    mv x9, a0
    li a0, 1
    add a0, x9, a0
    sd a0, 8(a1)
label_2:

    ld a0, 8(a1)
    li a0, 3
    sub a0, a0, a0
    seqz a0, a0
    beqz a0, label_3

    ld a0, 8(a1)
    li a0, 1
    add a0, a0, a0
    sd a0, 8(a1)
    j label_4
label_3:

label_4:

    # Function epilogue
    ld ra, 8(sp)
    ld fp, 0(sp)
    addi sp, sp, 16
    ret
