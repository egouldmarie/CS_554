.globl primescounter
.text
primescounter:
    # Function prologue
    # Allocate stack
    addi sp, sp, -0
    # Variable array pointer in a0
    # s1<-range (entry-live)
    ld s1, 0(a0)

label_entry:
    # ENTRY
label_0:
    # result := 0
    li t0, 0
    mv s5, t0
label_1:
    # while range >= 2
    li t1, 2
    slt t0, s1, t1
    xori t0, t0, 1
    beqz t0, label_18
label_2:
    # count := 0
    li t0, 0
    mv s2, t0
label_3:
    # i := 2
    li t0, 2
    mv s4, t0
label_4:
    # while (i * i) <= range
    mul t0, s4, s4
    slt t0, s1, t0
    xori t0, t0, 1
    beqz t0, label_14
label_5:
    # k := range
    mv s3, s1
label_6:
    # if count > 0
    li t1, 0
    slt t0, t1, s2
    beqz t0, label_8
label_7:
    # skip
    # skip
    j label_13
label_8:
    # while k >= 1
    li t1, 1
    slt t0, s3, t1
    xori t0, t0, 1
    beqz t0, label_13
label_9:
    # if (k * i) = range
    mul t0, s3, s4
    sub t0, t0, s1
    seqz t0, t0
    beqz t0, label_11
label_10:
    # count := count + 1
    li t1, 1
    add t0, s2, t1
    mv s2, t0
    j label_12
label_11:
    # skip
    # skip
label_12:
    # k := k – 1
    li t1, 1
    sub t0, s3, t1
    mv s3, t0
    j label_8
label_13:
    # i := i + 1
    li t1, 1
    add t0, s4, t1
    mv s4, t0
    j label_4
label_14:
    # if count > 0
    li t1, 0
    slt t0, t1, s2
    beqz t0, label_16
label_15:
    # skip
    # skip
    j label_17
label_16:
    # result := 1 + result
    li t0, 1
    add t0, t0, s5
    mv s5, t0
label_17:
    # range := range – 1
    li t1, 1
    sub t0, s1, t1
    mv s1, t0
    j label_1
label_18:
    # output := result
    mv s1, s5
label_exit:
    # EXIT

    # Function epilogue
    # Deallocate stack
    addi sp, sp, 0
    # output<-s1 (exit-live)
    sd s1, 32(a0)
    ret