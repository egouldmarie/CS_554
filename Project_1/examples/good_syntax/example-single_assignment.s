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
    # Function epilogue
    ld ra, 8(sp)
    ld fp, 0(sp)
    addi sp, sp, 16
    ret
