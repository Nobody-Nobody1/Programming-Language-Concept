class SimpleVM:
    def __init__(self):
        self.stack = []
        self.program = 0
    
    def execute(self, bytecode):
        self.program = 0  # Reset program counter
        
        bytecode_length = len(bytecode)

        while self.program < bytecode_length:

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
                
            elif instruction == 0x80:  # CLEAR instruction or 128
                self.stack.clear()
                self.program += 1
            
            elif instruction == 0x90:  # STORE instruction or 144
                if self.stack:
                    value = self.stack.pop()
                    with open('vm_store.txt', 'w') as f:
                        f.write(str(value))
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in STORE instruction")
                
            elif instruction == 0xA0:  # LOAD instruction or 160
                try:
                    with open('vm_store.txt', 'r') as f:
                        value = int(f.read())
                    self.stack.append(value)
                    self.program += 1
                except FileNotFoundError:
                    raise FileNotFoundError("No stored value found for LOAD instruction")
                
            else:
                raise ValueError(f"Unknown instruction {instruction} at position {self.program}")
        return self.stack