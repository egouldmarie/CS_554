.globl example13_fibonacci
.text
example13_fibonacci:
    # Function prologue
    addi sp, sp, -8
    # Variable array pointer in a0


    # literal = 0
    li t0, 0
    sd t0, 0(sp)

    # a := 
    ld t0, 0(sp)
    sd t0, 0(a0)

    # literal = 1
    li t0, 1
    sd t0, 0(sp)

    # b := 
    ld t0, 0(sp)
    sd t0, 8(a0)

    # literal = 0
    li t0, 0
    sd t0, 0(sp)

    # z := 
    ld t0, 0(sp)
    sd t0, 40(a0)

    # While Statement
while_label_1:

    # Condition

    # var n
    ld t0, 16(a0)
    sd t0, 0(sp)

    # var z
    ld t0, 40(a0)
    sd t0, 8(sp)

    # Equality
    ld t1, 8(sp)
    ld t0, 0(sp)
    sub t0, t0, t1
    seqz t0, t0
    sd t0, 0(sp)

    # NOT
    ld t0, 0(sp)
    seqz t0, t0
    sd t0, 0(sp)
    ld t0, 0(sp)

    beqz t0, end_label_1

    # Do

    # var a
    ld t0, 0(a0)
    sd t0, 0(sp)

    # var b
    ld t0, 8(a0)
    sd t0, 8(sp)

    # Addition
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)

    # t := 
    ld t0, 0(sp)
    sd t0, 32(a0)

    # var b
    ld t0, 8(a0)
    sd t0, 0(sp)

    # a := 
    ld t0, 0(sp)
    sd t0, 0(a0)

    # var t
    ld t0, 32(a0)
    sd t0, 0(sp)

    # b := 
    ld t0, 0(sp)
    sd t0, 8(a0)

    # var n
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

    # n := 
    ld t0, 0(sp)
    sd t0, 16(a0)

    # literal = 0
    li t0, 0
    sd t0, 0(sp)

    # z := 
    ld t0, 0(sp)
    sd t0, 40(a0)

    j while_label_1

    # Od
end_label_1:

    # var a
    ld t0, 0(a0)
    sd t0, 0(sp)

    # output := 
    ld t0, 0(sp)
    sd t0, 24(a0)

    # Function epilogue
    addi sp, sp, 8
    ret
