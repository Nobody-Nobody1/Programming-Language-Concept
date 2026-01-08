# NOTES THAT MIGHT BE USEFUL WHEN LOOKING AT THE DOCUMENTATION

R1, R2, R3 refers to memory registers, do not use in actual code since this is only for the README.md file

All commands aside from the MOVE command use the value already in memory registers

All inputs should be split by a comma otherwise you will get an error.

# HOW TO USE

clone repository using ` git clone Nobody-Nobody1/Virtual-Machine`

# COMMANDS WITH EXAMPLES

## INPUT
`MOVE` has 2 inputs such as `MOVE R1, 10` where R1 is getting 10

## OUTPUT

`PRINT` has 1 input such as `PRINT R1` where it will print whatever is in R1

`PRINTALL` has 0 inputs such as `PRINTALL` where it will print all registers

## MATH COMMANDS
`ADD` has 3 inputs such as `ADD R1, R2, R3` where R1 + R2 = R3

`SUB` has 3 inputs such as `SUB R1, R2, R3` where R1 - R2 = R3

`DIV` has 3 inputs such as `DIV R1, R2, R3` where R1 // R2 = R3 and if R3 is 0, it raises ZeroDivisionError

`MUL` has 3 inputs such as `MUL R1, R2, R3` where R1 * R2 = R3

## OTHER

`HALT` has 0 inputs such as `HALT` where once it reaches this command, it will stop

`HELP` has 0 inputs such as `HELP` where it will print README.md once it reaches this and stops the program