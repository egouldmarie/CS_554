# Assignment: Team Warmup Exercise: Optimizing the Emulator

## Completed by the Raspberry Pi group:
**Authors: Emma Gould      (egould@unm.edu)**<br/>
         **Nathan J. Rowe  (nrowe1@unm.edu)**<br/>
         **Qinghong Shao   (qinghongshao@unm.edu)**<br/>
         **Warren D. Craft (wdcraft@unm.edu)**<br/>

## Assignment Description/Details from CANVAS Course Site

> Available until Sep 21 at 11:59pm Sep 21 at 11:59pm
> Due Sep 21 at 11:59pm Sep 21 at 11:59pm
> 
> Put together the best ideas from your team members' solutions,
> and brainstorm to further improve the um emulator from the homework
> exercises.
> 
> Make sure that your team's emulator is able to execute this program:
> umix.umDownload umix.um
> 
> Then, report the performance of the emulator for sandmark.
> 
> This time, in addition to timing on b146-46.cs.unm.edu, time it on
> risc-machine-2.cs.unm.edu as well.
> 
> Keep in mind, this submission will count for everyone in your Groups
> for the compiler project group.

## Overview

instead of taking our fastest emulator, we focused on an emulator
in C++ that was not even quite completing the sandmark.um criterion …

got that working to be able to run sandmark, with an initial execution
time on the b146-46.cs.unm.edu machine of approx 3 mins, 40 secs.

initial timing investigations yielded the following data:

opcode	mean time (ns)	# calls	weighted (total time, secs)
0	    18.984	        356404848	        6.77
1	    41.898	        979571632	       41.04
2	    70.349	        747283504	       52.57
3	    15.056	         92344429	        1.39
4	    15.191	         40860531	        0.62
5	    19.871	          4987085	        0.10
6	    15.165	        389368029	        5.90
8	   189.758	         91964700	       17.45
9	   124.42	         91949290	       11.44
10	   293.399	             2946	        0.00
12	    38.122	        395373297	       15.07
13	    15.264	       2365891287	       36.11

gradual improvements …

examples …



