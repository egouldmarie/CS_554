.globl example6_collatz
.text
example6_collatz:
    # Function prologue
    # Variable array pointer in a0


    # var input
    ld t0, 0(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # n := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 8(a0)

    # literal = 0
    li t0, 0
    addi sp, sp, -8
    sd t0, 0(sp)

    # steps := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 40(a0)

    # While Statement
while_label_1:

    # Condition

    # var n
    ld t0, 8(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # literal = 1
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

    # Do

    # var n
    ld t0, 8(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # rem := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 32(a0)

    # literal = 0
    li t0, 0
    addi sp, sp, -8
    sd t0, 0(sp)

    # quot := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 24(a0)

    # While Statement
while_label_2:

    # Condition

    # var rem
    ld t0, 32(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # literal = 1
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

    beqz t0, end_label_2

    # Do

    # var rem
    ld t0, 32(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # literal = 2
    li t0, 2
    addi sp, sp, -8
    sd t0, 0(sp)

    # Subtraction
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    sub t0, t0, t1
    sd t0, 0(sp)

    # rem := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 32(a0)

    # var quot
    ld t0, 24(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # literal = 1
    li t0, 1
    addi sp, sp, -8
    sd t0, 0(sp)

    # Addition
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)

    # quot := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 24(a0)

    j while_label_2

    # Od
end_label_2:

    # If Statement

    # var rem
    ld t0, 32(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # literal = 0
    li t0, 0
    addi sp, sp, -8
    sd t0, 0(sp)

    # Equality
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    sub t0, t0, t1
    seqz t0, t0
    sd t0, 0(sp)
    ld t0, 0(sp)
    addi sp, sp, 8

    beqz t0, else_label_3

    # var quot
    ld t0, 24(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # n := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 8(a0)
    j end_label_3

else_label_3:

    # literal = 3
    li t0, 3
    addi sp, sp, -8
    sd t0, 0(sp)

    # var n
    ld t0, 8(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # Multiplication
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    mul t0, t0, t1
    sd t0, 0(sp)

    # literal = 1
    li t0, 1
    addi sp, sp, -8
    sd t0, 0(sp)

    # Addition
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)

    # n := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 8(a0)

end_label_3:

    # var steps
    ld t0, 40(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # literal = 1
    li t0, 1
    addi sp, sp, -8
    sd t0, 0(sp)

    # Addition
    ld t1, 0(sp)
    addi sp, sp, 8
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)

    # steps := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 40(a0)

    j while_label_1

    # Od
end_label_1:

    # var steps
    ld t0, 40(a0)
    addi sp, sp, -8
    sd t0, 0(sp)

    # output := 
    ld t0, 0(sp)
    addi sp, sp, 8
    sd t0, 16(a0)

    # Function epilogue
    ret
