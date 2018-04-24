#!/usr/bin/env python
import sys

#Command Line Arguements are stored in list argv
numArgs = len(sys.argv) - 1
sum = 0

#Iterate through each element and add to the sum
for n in range (1, len(sys.argv)):
    sum = sum + int(sys.argv[n])

#use the print function to output the sum
print(sum)
