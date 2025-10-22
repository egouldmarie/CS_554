.globl example1_factorial
.text
example1_factorial:
    # Function prologue
    # Variable array pointer in a0


    # var x
    ld t0, 8(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # y := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 16(a0)

    # n = 1
    li t0, 1
    addi sp, sp, -8
    sd t0, 0(sp)

    # z := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 24(a0)

    # While Statement
label_1:

    # var y
    ld t0, 16(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # n = 1
    li t0, 1
    addi sp, sp, -8
    sd t0, 0(sp)

    # Greater Than
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    slt t0, t1, t0
    sd t0, 0(sp)
    ld t0, 0(sp)
    addi sp, sp, 8

    beqz t0, end_label_1

    # var z
    ld t0, 24(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # var y
    ld t0, 16(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # Multiplication
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    mul t0, t0, t1
    sd t0, 0(sp)

    # z := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 24(a0)

    # var y
    ld t0, 16(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # n = 1
    li t0, 1
    addi sp, sp, -8
    sd t0, 0(sp)

    # Subtraction
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    sub t0, t0, t1
    sd t0, 0(sp)

    # y := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 16(a0)
    j label_1

end_label_1:

    # n = 0
    li t0, 0
    addi sp, sp, -8
    sd t0, 0(sp)

    # y := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 16(a0)

    # var z
    ld t0, 24(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # output := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 0(a0)

    # Function epilogue
    ret
