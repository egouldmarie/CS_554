.globl example_single_assignment
.text
example_single_assignment:
    # Function prologue
    addi sp, sp, -0
    # Variable array pointer in a0


    # literal = 3
    li t0, 3
    sd t0, 0(sp)

    # x := 
    ld t0, 0(sp)
    sd t0, 0(a0)

    # Function epilogue
    addi sp, sp, 0
    ret
