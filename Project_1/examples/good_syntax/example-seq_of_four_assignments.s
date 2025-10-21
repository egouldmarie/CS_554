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
    li x10, 4
    li x11, 2
    mul x12, x11, x9
    add x13, x10, x12
    mv x14, x13
    add x15, x9, x14
    sd x15, 24(a1)
    ld a0, 24(a1)
    li a0, 4
    sub a0, a0, a0
    sd a0, 0(a1)
    # Function epilogue
    ld ra, 8(sp)
    ld fp, 0(sp)
    addi sp, sp, 16
    ret
