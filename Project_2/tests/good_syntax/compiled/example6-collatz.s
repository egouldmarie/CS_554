.globl example6_collatz
.text
example6_collatz:
    # Function prologue
    # Allocate stack
    addi sp, sp, -0
    # Variable array pointer in a0
    # s1<-input
    ld s1, 0(a0)
    # s2<-n
    ld s2, 8(a0)
    # s3<-output
    ld s3, 16(a0)
    # s4<-quot
    ld s4, 24(a0)
    # s5<-rem
    ld s5, 32(a0)
    # s6<-steps
    ld s6, 40(a0)

label_0:
    # Label 0: n := input
    mv s2, s1
label_1:
    # Label 1: steps := 0
    li t0, 0
    mv s6, t0
label_2:
    # Label 2: while: n > 1
    li t1, 1
    slt t0, t1, s2
    beqz t0, label_12
label_3:
    # Label 3: rem := n
    mv s5, s2
label_4:
    # Label 4: quot := 0
    li t0, 0
    mv s4, t0
label_5:
    # Label 5: while: rem > 1
    li t1, 1
    slt t0, t1, s5
    beqz t0, label_8
label_6:
    # Label 6: rem := rem – 2
    li t1, 2
    sub t0, s5, t1
    mv s5, t0
label_7:
    # Label 7: quot := quot + 1
    li t1, 1
    add t0, s4, t1
    mv s4, t0
    j label_5
label_8:
    # Label 8: if: rem = 0
    li t1, 0
    sub t0, s5, t1
    seqz t0, t0
    beqz t0, label_10
label_9:
    # Label 9: n := quot
    mv s2, s4
label_11:
    # Label 11: steps := steps + 1
    li t1, 1
    add t0, s6, t1
    mv s6, t0
    j label_2
label_10:
    # Label 10: n := 3 * n + 1
    li t0, 3
    mul t0, t0, s2
    li t1, 1
    add t0, t0, t1
    mv s2, t0
label_12:
    # Label 12: output := steps
    mv s3, s6
    # Function epilogue
    # Deallocate stack
    addi sp, sp, 0
    # input<-s1
    sd s1, 0(a0)
    # n<-s2
    sd s2, 8(a0)
    # output<-s3
    sd s3, 16(a0)
    # quot<-s4
    sd s4, 24(a0)
    # rem<-s5
    sd s5, 32(a0)
    # steps<-s6
    sd s6, 40(a0)
    ret