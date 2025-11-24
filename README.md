# CS 554 (2025 Fall)

Repository for storing, sharing, and collaborating on code used and
constructed by the "Raspberry Pi" compiler project group (Gould,
Rowe, Shao, & Craft) for CS 554 (Compiler Construction, 2025 Fall,
instructor Darko Stefanovic) at the University of New Mexico.

About mid-semester, the Raspberry Pi group was reduced to the trio
Gould, Shao, & Craft, with the departure of Rowe.

## Contents

Assignments and folders for assignment content proceed in the following
order:

## (1) Team_Warmup_Benchmarking (9/14/2025)

An initial team exercise, in part designed to compare performance
of the CS department's b146-46 and risc-machine-2 machines, but also
intended to provide some impetus to project group members to begin
working together and develop some useful means of communication for
future group project work. The explicit assignment was to compare the
performance of various workloads between risc-machine-2.cs.unm.edu
and b146-46.cs.unm.edu machines and produce a report (PDF file), with
at least one workload per team member.

## (2) Team_Warmup_Optimizing_Emulator (9/21/2025)

The assignment was to put together the best ideas from the team
members' solutions, and brainstorm to further improve the um emulator
generated during the earlier homework exercises, then test and report
on the performance of the emulator for sandmark on both the b146 and
risc-v machines. Our work focused on working out some remaining bugs
in one of our emulators in C++ and then working on refinements to
bring down its sandmark execution time.

## (3) Team_Warmup_Factorial (9/23/2025)

In the team factorial-related work, the assignment was to test and
report on the performance of the emulator on two newer factorial-
computing programs, on both the b146 and risc-v machines.

## (4) Project_1 (9/23/2025 -- 10/28/2025)

Project 1 was titled "Simple Code Generation," and the goal of
the project was to create a compiler to translate programs in the
simple canonical imperative WHILE language into RISC-V assembly code.
The compiler also generates a specialized C main program for
each WHILE program, responsible for all input/output.
The resulting assembly and C programs can then be compiled together
using gcc on a risc-v machine and the resulting executable run on
that same machine.

See the Project_1_Assignment.pdf file (in the Projec_1 folder) for
instructor-supplied assignment details.

## (5) Project_2 (11/05/2025 -- 12/05/2025)

Project 2 was titled "Program analyses, code transformations, and
improved code generation."
