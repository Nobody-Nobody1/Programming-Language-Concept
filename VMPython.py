import ByteCodeReader

class SimpleVM:
    def __init__(self):
        self.stack = []
        self.program = 0
    
    def execute(self, bytecode):
        self.program = 0  # Reset program counter
        while self.program < len(bytecode):
            instruction = bytecode[self.program]
            if instruction == 0x10:  # PUSH instruction or 16
                value = bytecode[self.program + 1]
                self.stack.append(value)
                self.program += 2

            elif instruction == 0x20:  # ADD instruction or 32
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a + b)
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in ADD instruction")
                
            elif instruction == 0x30:  # SUB instruction or 48
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a - b)
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in SUB instruction")
                
            elif instruction == 0x40:  # MUL instruction or 64
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a * b)
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in MUL instruction")
                
            elif instruction == 0x50:  # DIV instruction or 80
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    if b != 0:
                        self.stack.append(a // b)
                        self.program += 1
                    else:
                        raise ZeroDivisionError("Division by zero")
                else:
                    raise ValueError("Stack underflow in DIV instruction")
                
            elif instruction == 0x60:  # HALT instruction or 96
                break

            elif instruction == 0x70:  # PRINT instruction or 112
                if self.stack:
                    print(self.stack.pop())
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in PRINT instruction")
                
            else:
                raise ValueError(f"Unknown instruction: {instruction}")
        return self.stack