.globl countTriangularNumbers
.text
countTriangularNumbers:
    # Function prologue
    addi sp, sp, -8
    # Variable array pointer in a0

    li t0, 0
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 24(a0)
    li t0, 0
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 48(a0)
    li t0, 1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 32(a0)
    li t0, 0
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 0(a0)
while_label_1:
    ld t0, 16(a0)
    sd t0, 0(sp)
    ld t0, 8(a0)
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    slt t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, end_label_1
while_label_2:
    ld t0, 48(a0)
    sd t0, 0(sp)
    ld t0, 16(a0)
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    slt t0, t1, t0
    xori t0, t0, 1
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, end_label_2
    ld t0, 48(a0)
    sd t0, 0(sp)
    ld t0, 32(a0)
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 48(a0)
    ld t0, 48(a0)
    sd t0, 0(sp)
    ld t0, 16(a0)
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    sub t0, t0, t1
    seqz t0, t0
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, else_label_3
    li t0, 1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 24(a0)
    ld t0, 16(a0)
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 48(a0)
    j end_label_3
else_label_3:
    # [skip]0
end_label_3:
    ld t0, 32(a0)
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 32(a0)
    j while_label_2
end_label_2:
    ld t0, 24(a0)
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    sub t0, t0, t1
    seqz t0, t0
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, else_label_4
    ld t0, 0(a0)
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 0(a0)
    j end_label_4
else_label_4:
    # [skip]1
end_label_4:
    li t0, 0
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 24(a0)
    li t0, 0
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 48(a0)
    li t0, 1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 32(a0)
    ld t0, 16(a0)
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 16(a0)
    j while_label_1
end_label_1:
    ld t0, 0(a0)
    sd t0, 0(sp)
    ld t0, 0(sp)
    sd t0, 40(a0)
    # Function epilogue
    addi sp, sp, 8
    ret