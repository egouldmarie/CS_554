.globl example1_factorial
.text
example1_factorial:
    # Function prologue
    addi sp, sp, -8
    # Variable array pointer in a0


    # var x
    ld t0, 8(a0)
    sd t0, 0(sp)

    # y := 
    ld t0, 0(sp)
    sd t0, 16(a0)

    # literal = 1
    li t0, 1
    sd t0, 0(sp)

    # z := 
    ld t0, 0(sp)
    sd t0, 24(a0)

    # While Statement
while_label_1:

    # Condition

    # var y
    ld t0, 16(a0)
    sd t0, 0(sp)

    # literal = 1
    li t0, 1
    sd t0, 8(sp)

    # Greater Than
    ld t1, 8(sp)
    ld t0, 0(sp)
    slt t0, t1, t0
    sd t0, 0(sp)
    ld t0, 0(sp)

    beqz t0, end_label_1

    # Do

    # var z
    ld t0, 24(a0)
    sd t0, 0(sp)

    # var y
    ld t0, 16(a0)
    sd t0, 8(sp)

    # Multiplication
    ld t1, 8(sp)
    ld t0, 0(sp)
    mul t0, t0, t1
    sd t0, 0(sp)

    # z := 
    ld t0, 0(sp)
    sd t0, 24(a0)

    # var y
    ld t0, 16(a0)
    sd t0, 0(sp)

    # literal = 1
    li t0, 1
    sd t0, 8(sp)

    # Subtraction
    ld t1, 8(sp)
    ld t0, 0(sp)
    sub t0, t0, t1
    sd t0, 0(sp)

    # y := 
    ld t0, 0(sp)
    sd t0, 16(a0)

    j while_label_1

    # Od
end_label_1:

    # literal = 0
    li t0, 0
    sd t0, 0(sp)

    # y := 
    ld t0, 0(sp)
    sd t0, 16(a0)

    # var z
    ld t0, 24(a0)
    sd t0, 0(sp)

    # output := 
    ld t0, 0(sp)
    sd t0, 0(a0)

    # Function epilogue
    addi sp, sp, 8
    ret
