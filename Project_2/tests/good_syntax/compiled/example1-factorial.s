.globl example1_factorial
.text
example1_factorial:
    # Function prologue
    # Allocate stack
    addi sp, sp, -0
    # Variable array pointer in a0
    # s1<-output
    ld s1, 0(a0)
    # s2<-x
    ld s2, 8(a0)
    # s3<-y
    ld s3, 16(a0)
    # s4<-z
    ld s4, 24(a0)

label_entry:
    # ENTRY
label_0:
    # y := x
    mv s3, s2
label_1:
    # z := 1
    li t0, 1
    mv s4, t0
label_2:
    # while y > 1
    li t1, 1
    slt t0, t1, s3
    beqz t0, label_5
label_3:
    # z := z * y
    mul t0, s4, s3
    mv s4, t0
label_4:
    # y := y – 1
    li t1, 1
    sub t0, s3, t1
    mv s3, t0
    j label_2
label_5:
    # y := 0
    li t0, 0
    mv s3, t0
label_6:
    # output := z
    mv s1, s4
label_exit:
    # EXIT

    # Function epilogue
    # Deallocate stack
    addi sp, sp, 0
    # output<-s1
    sd s1, 0(a0)
    # x<-s2
    sd s2, 8(a0)
    # y<-s3
    sd s3, 16(a0)
    # z<-s4
    sd s4, 24(a0)
    ret