virtual machine using hexadecimal commands or text commands

run test.sh for actual script and test2.sh to see ByteCodeReader.py convert Bytecode.txt to array

PUSH is 16 and allows you to push the next line after it to self.stack

ADD is 32 and allows you to add the top 2 values in self.stack

SUB is 48 and allows you to subtract the top 2 values in self.stack

MUL is 64 and allows you to mutliply the top 2 values in self.stack

DIV is 80 and allows you to divide the top 2 values in self.stack

HALT is 96 and stops when it reaches this

PRINT is 112 and prints self.stack

CLEAR is 128 and clears self.stack fully

STORE is 144 and removes last index and writes to vm_store.txt

LOAD is 160 and adds whatever is in vm_store.txt

JUMP is 176 and jumps to whatever line the next command is

JUMPIFZERO is 192 and checks whether popped value from self.stack is 0, if so then it jumps to whatever line the next command is else it doesn't do anything