.text
.globl generated_function
generated_function:
    # Function prologue
    addi sp, sp, -16
    sd ra, 8(sp)
    sd fp, 0(sp)
    addi fp, sp, 16
    # Variable array pointer in a1

    mv x9, x8
    li x10, 0
    mv x11, x10
label_1:

    li x12, 1
    slt x13, x12, x9
    beqz x13, label_2

    mv x14, x9
    li x15, 0
    sd x15, 24(a1)
label_3:

    li a0, 1
    slt a0, a0, x14
    beqz a0, label_4

    li a0, 2
    sub a0, x14, a0
    mv x14, a0
    ld a0, 24(a1)
    li a0, 1
    add a0, a0, a0
    sd a0, 24(a1)
    j label_3
label_4:

    li a0, 0
    sub a0, x14, a0
    seqz a0, a0
    beqz a0, label_5

    ld a0, 24(a1)
    mv x9, a0
    j label_6
label_5:

    li a0, 3
    mul a0, a0, x9
    li a0, 1
    add a0, a0, a0
    mv x9, a0
label_6:

    li a0, 1
    add a0, x11, a0
    mv x11, a0
    j label_1
label_2:

    sd x11, 16(a1)
    # Function epilogue
    ld ra, 8(sp)
    ld fp, 0(sp)
    addi sp, sp, 16
    ret
