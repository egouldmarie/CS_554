.globl example6_collatz
.text
example6_collatz:
    # Function prologue
    addi sp, sp, -8
    # Variable array pointer in a0
    # s1<-input
    ld s1, 0(a0)
    # s2<-input
    ld s2, 8(a0)
    # s3<-input
    ld s3, 16(a0)
    # s4<-input
    ld s4, 24(a0)
    # s5<-input
    ld s5, 32(a0)
    # s6<-input
    ld s6, 40(a0)

    # label = 0
    ld t0, s1
    sd t0, 0(sp)
    ld s2, 0(sp)

    # label = 1
    li t0, 0
    sd t0, 0(sp)
    ld s6, 0(sp)

while_label_1:
    # label = 2
    ld t0, s2
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    slt t0, t1, t0
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, end_label_1

    # label = 3
    ld t0, s2
    sd t0, 0(sp)
    ld s5, 0(sp)

    # label = 4
    li t0, 0
    sd t0, 0(sp)
    ld s4, 0(sp)

while_label_2:
    # label = 5
    ld t0, s5
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    slt t0, t1, t0
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, end_label_2

    # label = 6
    ld t0, s5
    sd t0, 0(sp)
    li t0, 2
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    sub t0, t0, t1
    sd t0, 0(sp)
    ld s5, 0(sp)

    # label = 7
    ld t0, s4
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    ld s4, 0(sp)

    j while_label_2
end_label_2:
    # label = 8
    ld t0, s5
    sd t0, 0(sp)
    li t0, 0
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    sub t0, t0, t1
    seqz t0, t0
    sd t0, 0(sp)
    ld t0, 0(sp)
    beqz t0, else_label_3

    # label = 9
    ld t0, s4
    sd t0, 0(sp)
    ld s2, 0(sp)

    j end_label_3
else_label_3:
    # label = 10
    li t0, 3
    sd t0, 0(sp)
    ld t0, s2
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    mul t0, t0, t1
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    ld s2, 0(sp)

end_label_3:
    # label = 11
    ld t0, s6
    sd t0, 0(sp)
    li t0, 1
    sd t0, 8(sp)
    ld t1, 8(sp)
    ld t0, 0(sp)
    add t0, t0, t1
    sd t0, 0(sp)
    ld s6, 0(sp)

    j while_label_1
end_label_1:
    # label = 12
    ld t0, s6
    sd t0, 0(sp)
    ld s3, 0(sp)


    # Function epilogue
    addi sp, sp, 8
    # output<-s1
    sd s1, 0(a0)
    # output<-s2
    sd s2, 8(a0)
    # output<-s3
    sd s3, 16(a0)
    # output<-s4
    sd s4, 24(a0)
    # output<-s5
    sd s5, 32(a0)
    # output<-s6
    sd s6, 40(a0)
    ret