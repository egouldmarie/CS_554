.globl example_if_then_else_testing_relational_ops
.text
example_if_then_else_testing_relational_ops:
    # Function prologue
    addi sp, sp, -16
    # Variable array pointer in a0

    ld t0, 0(a0)
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 16(a0)
    ld t0, 16(a0)
    sd t0, 0(sp)
    li t0, 0
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    sub t0, t0, t1
    seqz t0, t0
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, else_label_1
    li t0, 1
    sd t0, 0(sp)
    li t0, 0
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    li t0, 0
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    mul t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 24(a0)
    j end_label_1
else_label_1:
    ld t0, 16(a0)
    sd t0, 0(sp)
    li t0, 0
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    slt t0, t1, t0
    sd t0, 0(sp)
    ld t0, 16(a0)
    sd t0, 8(sp)
    li t0, 10
    sd t0, 16(sp)
    ld t1, 16(sp)
    ld t0, 8(sp)
    slt t0, t0, t1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    and t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, else_label_2
    li t0, 2
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 24(a0)
    j end_label_2
else_label_2:
    ld t0, 16(a0)
    sd t0, 0(sp)
    li t0, 10
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    slt t0, t0, t1
    xori t0, t0, 1
    sd t0, 0(sp)
    ld t0, 16(a0)
    sd t0, 8(sp)
    li t0, 20
    sd t0, 16(sp)
    ld t1, 16(sp)
    ld t0, 8(sp)
    slt t0, t1, t0
    xori t0, t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    and t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, else_label_3
    li t0, 3
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 24(a0)
    j end_label_3
else_label_3:
    li t0, 4
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 24(a0)
end_label_3:
end_label_2:
end_label_1:
    ld t0, 24(a0)
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 8(a0)
    # Function epilogue
    addi sp, sp, 16
    ret