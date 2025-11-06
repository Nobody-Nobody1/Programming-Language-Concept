import math


class SimpleVM:
    def __init__(self):
        self.stack = []                # stack for calculations
        self.memory = {}              # memory (key -> value)
        self.program_counter = 0      # current instruction index
        self.call_stack = []          # return addresses for CALL/RET
        self.halted = False

    def reset(self):
        """Reset VM state to initial empty state."""
        self.stack.clear()
        self.memory.clear()
        self.program_counter = 0
        self.call_stack.clear()
        self.halted = False

    def _require_stack(self, n, instr):
        if len(self.stack) < n:
            raise IndexError(f"Not enough values on stack for {instr}: need {n}, have {len(self.stack)}")

    def step(self, bytecode, output_callback=None):
        """Execute a single instruction at the current program_counter.
        Returns True if execution should continue, False if halted or end reached.
        If output_callback is provided it will be called with any textual output
        from PRINT or MEM_DEBUG; otherwise output goes to stdout.
        """
        if self.halted:
            return False

        if self.program_counter >= len(bytecode):
            # end of program
            self.halted = True
            return False

        instr = bytecode[self.program_counter]

        def out(s):
            if output_callback:
                output_callback(str(s))
            else:
                print(s)

        # dispatch
        if instr == 'PUSH':
            if self.program_counter + 1 >= len(bytecode):
                raise IndexError('PUSH instruction missing operand')
            val = bytecode[self.program_counter + 1]
            # allow numeric strings to be converted
            if isinstance(val, str) and val.isdigit():
                val = int(val)
            self.stack.append(val)
            self.program_counter += 2
            return True

        if instr == 'ADD':
            self._require_stack(2, 'ADD')
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)
            self.program_counter += 1
            return True

        if instr == 'SUBTRACT':
            self._require_stack(2, 'SUBTRACT')
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)
            self.program_counter += 1
            return True

        if instr == 'DIVIDE':
            self._require_stack(2, 'DIVIDE')
            b = self.stack.pop()
            a = self.stack.pop()
            if b == 0:
                raise ZeroDivisionError('Division by zero')
            # integer division
            self.stack.append(a // b)
            self.program_counter += 1
            return True

        if instr == 'MULTIPLY':
            self._require_stack(2, 'MULTIPLY')
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)
            self.program_counter += 1
            return True

        if instr == 'MEM_DEBUG':
            out(self.memory)
            self.program_counter += 1
            return True

        if instr == 'STORE':
            if self.program_counter + 1 >= len(bytecode):
                raise IndexError('STORE instruction missing key')
            self._require_stack(1, 'STORE')
            key = bytecode[self.program_counter + 1]
            val = self.stack.pop()
            self.memory[key] = val
            self.program_counter += 2
            return True

        if instr == 'STORE_COPY':
            if self.program_counter + 1 >= len(bytecode):
                raise IndexError('STORE_COPY instruction missing key')
            self._require_stack(1, 'STORE_COPY')
            key = bytecode[self.program_counter + 1]
            val = self.stack[-1]
            self.memory[key] = val
            self.program_counter += 2
            return True

        if instr == 'LOAD':
            if self.program_counter + 1 >= len(bytecode):
                raise IndexError('LOAD instruction missing key')
            key = bytecode[self.program_counter + 1]
            if key not in self.memory:
                raise KeyError(f"LOAD failed: key '{key}' not found in memory")
            self.stack.append(self.memory[key])
            self.program_counter += 2
            return True

        if instr == 'COMMENT':
            if self.program_counter + 1 < len(bytecode):
                self.program_counter += 2
            else:
                self.program_counter += 1
            return True

        if instr == 'PRINT':
            self._require_stack(1, 'PRINT')
            out(self.stack[-1])
            self.program_counter += 1
            return True

        if instr == 'HALT':
            self.halted = True
            return False

        if instr == 'INPUT':
            try:
                user_input = int(input('Enter an integer: '))
            except ValueError:
                raise ValueError('Invalid integer input')
            self.stack.append(user_input)
            self.program_counter += 1
            return True

        if instr == 'SQUARE':
            self._require_stack(1, 'SQUARE')
            v = self.stack.pop()
            self.stack.append(v * v)
            self.program_counter += 1
            return True

        if instr == 'SQRT':
            self._require_stack(1, 'SQRT')
            v = int(self.stack.pop())
            if v < 0:
                raise ValueError('Cannot compute square root of negative number')
            # integer sqrt
            self.stack.append(math.isqrt(v))
            self.program_counter += 1
            return True

        if instr == 'BINARY':
            self._require_stack(1, 'BINARY')
            v = int(self.stack.pop())
            self.stack.append(bin(v)[2:])
            self.program_counter += 1
            return True

        if instr == 'WAIT':
            input('Press Enter to continue...')
            self.program_counter += 1
            return True

        if instr == 'IF':
            self._require_stack(1, 'IF')
            cond = self.stack.pop()
            if self.program_counter + 1 >= len(bytecode):
                raise IndexError('IF instruction missing target')
            target = bytecode[self.program_counter + 1]
            try:
                target = int(target)
            except Exception:
                raise ValueError('IF target must be an integer index')
            if cond != 0:
                if target < 0 or target >= len(bytecode):
                    raise IndexError('IF target out of range')
                self.program_counter = target
            else:
                self.program_counter += 2
            return True

        if instr == 'JUMP':
            if self.program_counter + 1 >= len(bytecode):
                raise IndexError('JUMP instruction missing target')
            target = bytecode[self.program_counter + 1]
            try:
                target = int(target)
            except Exception:
                raise ValueError('JUMP target must be an integer index')
            if target < 0 or target >= len(bytecode):
                raise IndexError('JUMP target out of range')
            self.program_counter = target
            return True

        if instr == 'DUP':
            self._require_stack(1, 'DUP')
            self.stack.append(self.stack[-1])
            self.program_counter += 1
            return True

        if instr == 'POP':
            self._require_stack(1, 'POP')
            self.stack.pop()
            self.program_counter += 1
            return True

        if instr == 'SWAP':
            self._require_stack(2, 'SWAP')
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            self.program_counter += 1
            return True

        if instr == 'OVER':
            self._require_stack(2, 'OVER')
            self.stack.append(self.stack[-2])
            self.program_counter += 1
            return True

        if instr in ('EQ', 'LT', 'GT', 'LE', 'GE', 'NE'):
            self._require_stack(2, instr)
            b = self.stack.pop()
            a = self.stack.pop()
            res = 0
            if instr == 'EQ':
                res = 1 if a == b else 0
            elif instr == 'LT':
                res = 1 if a < b else 0
            elif instr == 'GT':
                res = 1 if a > b else 0
            elif instr == 'LE':
                res = 1 if a <= b else 0
            elif instr == 'GE':
                res = 1 if a >= b else 0
            elif instr == 'NE':
                res = 1 if a != b else 0
            self.stack.append(res)
            self.program_counter += 1
            return True

        if instr == 'CALL':
            if self.program_counter + 1 >= len(bytecode):
                raise IndexError('CALL instruction missing target')
            target = bytecode[self.program_counter + 1]
            try:
                target = int(target)
            except Exception:
                raise ValueError('CALL target must be an integer index')
            if target < 0 or target >= len(bytecode):
                raise IndexError('CALL target out of range')
            # push return address
            self.call_stack.append(self.program_counter + 2)
            self.program_counter = target
            return True

        if instr == 'RET':
            if not self.call_stack:
                raise IndexError('RET with empty call stack')
            self.program_counter = self.call_stack.pop()
            return True

        # unknown instruction
        raise ValueError(f'Unknown instruction: {instr}')

    def execute(self, bytecode, output_callback=None):
        """Run until HALT or end of bytecode. Returns when VM halts.
        output_callback is passed to step() to capture PRINT/MEM_DEBUG output.
        """
        while True:
            cont = self.step(bytecode, output_callback=output_callback)
            if not cont:
                break