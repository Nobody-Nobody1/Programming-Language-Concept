# Virtual-Machine
virtual machine, possibly in a collection of languages
Basing it off https://www.google.com/search?q=BASIC+computer+language+commands&sca_esv=a7a7f7107bf5a5bb&rlz=1CABASQ_enUS1031&sxsrf=AE3TifPWQ1RTpujA6yK65RrO8XAj5XpoUA%3A1762405699804&ei=Qy0MaZbnMOrl5NoPrvDp6Q0&ved=0ahUKEwjWlL_t4NyQAxXqMlkFHS54Ot0Q4dUDCBE&uact=5&oq=BASIC+computer+language+commands&gs_lp=Egxnd3Mtd2l6LXNlcnAiIEJBU0lDIGNvbXB1dGVyIGxhbmd1YWdlIGNvbW1hbmRzMgsQABiABBiRAhiKBTILEAAYgAQYhgMYigUyCxAAGIAEGIYDGIoFMgsQABiABBiGAxiKBTIFEAAY7wUyCBAAGIAEGKIESI0iUGFY9iBwAngBkAEAmAFioAHQBaoBATm4AQPIAQD4AQGYAgugArQGwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgUQABiABMICBhAAGBYYHpgDAIgGAZAGCpIHAzkuMqAHlyeyBwM3LjK4B54GwgcFMi05LjLIB0o&sclient=gws-wiz-serp&safe=active&ssui=on

JUST LOOK AT THE README.md FILE

Debugging:
PRINT to print calculations 
MEM_DEBUG to print memory 
COMMENT to create space or comments 
HALT to stop process when the counter reaches this command 
PUSH to add info 
INPUT to ask user for another integer 
BINARY to turn the last index into the binary version of it 
WAIT to wait until the user presses enter

Operands: 
ADD to add last 2 indexes 
SUBTRACT to subtract last 2 indexes 
MULTIPLY to multiply last 2 indexes 
DIVIDE to divide last 2 indexes
SQUARE to square last index
SQRT to find the square root of last index

Memory Management: 


Label support and assembler
---------------------------
This VM now supports symbolic labels in `ByteCode.txt`. Labels are declared on their own line with a trailing colon, for example:

```

Run the GUI
-----------

You can run the optional desktop GUI with:

```
python3 vm_gui.py
```

The GUI allows loading a bytecode file, stepping, running to completion, setting
an optional numeric breakpoint, and viewing stack/memory/console output.

loop_start:
	PUSH
	5
	PRINT
```

You can reference a label from a jump/conditional instruction (currently `IF`) by
using the label name as the operand:

```
PUSH
3
IF
loop_start

loop_start:
PUSH
5
PRINT
```

How it works
- The `ByteCodeReader.read_text_file_to_list()` function performs a two-pass assembly:
	- Pass 1 scans tokens and records label definitions and their instruction
		indices (it counts how many VM slots each opcode consumes so indices match
		what the VM expects).
	- Pass 2 emits a final list where label usages are replaced by integer indices
		and numeric strings are converted to ints.

Why this was added
- Labels improve readability and let you insert/remove instructions without recalculating numeric jump targets.

Notes and constraints
- Label declarations must be on their own line and end with a colon (`name:`).
- The assembler currently supports `PUSH`, `IF`, and `COMMENT` as multi-token
	opcodes (they consume a following operand). The mapping matches the VM's
	token consumption rules: `PUSH` consumes 2 slots (opcode + operand), `IF`
	consumes 2 slots (opcode + target), `COMMENT` consumes 2 slots.
- Forward references are allowed (you can reference labels declared later).
- If an `IF` or `PUSH` operand is missing or a label is undefined, the reader
	will raise a clear error before execution.

If you'd like, I can extend label support to a `JUMP` opcode, or allow labels
as `PUSH` operands (currently `PUSH` operands must be integers).

STORE / LOAD
------------
Two simple memory instructions were added:

- STORE <key>
	- Pops the top value from the stack and stores it in the VM memory under <key>.
	- <key> can be an integer literal or a string identifier in the bytecode.

- LOAD <key>
	- Pushes the value stored under <key> back onto the stack. If the key is
		not present a KeyError is raised.

Example (appended to `ByteCode.txt`):

```
PUSH
42
STORE
answer
LOAD
answer
PRINT
```

This will store 42 into memory under key `answer`, load it back onto the stack,
and print `42`.

Implemented features (summary)
------------------------------
The VM has been extended with a number of instructions and helpers. Below is a
concise reference of what's available now and short examples.

Control flow
- JUMP <target> — unconditional jump to instruction index <target>.
- IF — conditional jump: pops condition; next token is a numeric target index.
- CALL <target> / RET — call subroutine at <target> and return with RET.

Comparisons (push 1 for true, 0 for false)
- EQ, LT, GT, LE, GE, NE — pop two values (a, b) and push comparison result.

Stack helpers
- DUP — duplicate the top-of-stack value.
- POP — remove the top-of-stack value.
- SWAP — swap the top two values.
- OVER — push a copy of the second element onto the top.

Memory
- STORE <key> — pop value and store under <key>.
- STORE_COPY <key> — store value under <key> but keep it on the stack.
- LOAD <key> — push memory[<key>] onto the stack.
- MEM_DEBUG — prints the VM memory dictionary.

Math and misc
- ADD, SUBTRACT, MULTIPLY, DIVIDE — basic arithmetic (DIVIDE uses integer division).
- SQUARE, SQRT — square and integer square root (uses math.isqrt).
- BINARY — convert top value to a binary string (without '0b').
- INPUT — prompt for an integer and push it.
- WAIT — pause until Enter pressed.
- COMMENT — skip the next token.
- PRINT — print top of stack (non-destructive).
- HALT — stop execution.

Execution model
- The VM exposes a `step(bytecode, output_callback=None)` method which executes a
	single instruction and returns True to continue or False to stop. `execute()` runs
	until HALT or end-of-bytecode. `output_callback` allows the host (CLI or GUI)
	to capture textual output from PRINT and MEM_DEBUG.

Examples
- Loop with JUMP/IF (pseudo):

```
PUSH
10
loop_start:
PUSH
1
SUBTRACT
DUP
IF
loop_start
PRINT
```

- CALL/RET (pseudo):

```
CALL
func_start
HALT
func_start:
PUSH
42
PRINT
RET
```
