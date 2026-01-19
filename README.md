# NOTES THAT MIGHT BE USEFUL WHEN LOOKING AT THE DOCUMENTATION

R1, R2, R3 refers to memory registers, do not use in actual code since this is only for the README.md file

All commands aside from the MOVE command use the value already in memory registers

All inputs should be split by a comma otherwise you will get an error.

Add a boolean value to the last variable in the vm.execute to toggle getting self.registers
- (default is false)

Always put `PRINT_EXECUTED` at the end

# HOW TO USE

clone repository using ` git clone Nobody-Nobody1/Virtual-Machine`
use the run and debug in vscode to run it

## DATA MOVEMENT
`MOVE` has 2 inputs such as `MOVE R1, 10` where R1 is getting 10

## MATHMATICAL OPERATIONS
`ADD` has 3 inputs such as `ADD R1, R2, R3` where R1 + R2 = R3

`SUB` has 3 inputs such as `SUB R1, R2, R3` where R1 - R2 = R3

`DIV` has 3 inputs such as `DIV R1, R2, R3` where R1 // R2 = R3 and if R3 is 0, it raises ZeroDivisionError

`MUL` has 3 inputs such as `MUL R1, R2, R3` where R1 * R2 = R3

## OUTPUT AND DEBUGGING

`PRINT_MEMORY` has 0 inputs such as `PRINT_MEMORY` where it will print all registers

`PRINT_ARRAY` has 0 inputs such as `PRINT_ARRAY` where it will print how the bytecode file is seen

`PRINT_EXECUTED` has 0 inputs such as `PRINT_EXECUTED` where it will print the amount of executed instructions

## HELP COMMAND

`HELP` has 0 inputs such as `HELP` where it will print README.md once it reaches this and stops the program

## PROGRAM FLOW

`HALT` has 0 inputs such as `HALT` where once it reaches this command, it will stop

`NOOP` has 0 inputs such as `NOOP` where it won't do anything upon reaching this
