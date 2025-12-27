import ReadmeInteracter

class SimpleVM:
    def __init__(self):
        self.stack = []
        self.program = 0
    
    def execute(self, bytecode):
        
        bytecode_length = len(bytecode)

        while self.program <= bytecode_length:

            instruction = bytecode[self.program]

            if instruction == 0x10 or "PUSH":  # PUSH instruction or 16
                print("hello" + str(self.program))
                self.program += 1
                value = bytecode[self.program]
                self.stack.append(value)
                

            elif instruction == 0x20 or "ADD":  # ADD instruction or 32
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a + b)
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in ADD instruction")
                
            elif instruction == 0x30 or "SUB":  # SUB instruction or 48
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a - b)
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in SUB instruction")
                
            elif instruction == 0x40 or "MUL":  # MUL instruction or 64
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a * b)
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in MUL instruction")
                
            elif instruction == 0x50 or "DIV":  # DIV instruction or 80
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
                
            elif instruction == 0x60 or "HALT":  # HALT instruction or 96
                break

            elif instruction == 0x70 or "PRINT":  # PRINT instruction or 112
                if self.stack:
                    print(self.stack.pop())
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in PRINT instruction")
                
            elif instruction == 0x80 or "CLEAR":  # CLEAR instruction or 128
                self.stack.clear()
                self.program += 1
            
            elif instruction == 0x90 or "STORE":  # STORE instruction or 144
                if self.stack:
                    value = self.stack.pop()
                    with open('vm_store.txt', 'w') as f:
                        f.write(str(value))
                    self.program += 1
                else:
                    raise ValueError("Stack underflow in STORE instruction")
                
            elif instruction == 0xA0 or "LOAD":  # LOAD instruction or 160
                try:
                    with open('vm_store.txt', 'r') as f:
                        value = int(f.read())
                    self.stack.append(value)
                    self.program += 1
                except FileNotFoundError:
                    raise FileNotFoundError("No stored value found for LOAD instruction")

            elif instruction == 0xB0 or "JUMP": # JUMP instruction or 176
                target = bytecode[self.program + 1]
                self.program = target

            elif instruction == 0xC0 or "JUMPIFZERO": # JUMPIFZERO instruction or 192
                if self.stack:
                    value = self.stack.pop()
                    target = bytecode[self.program + 1]
                    if value == 0:
                        self.program = target
                    else:
                        self.program += 2
                else:
                    raise ValueError("Stack underflow in JUMPIFZERO instruction")
            
            elif instruction == 0xD0 or "HELP": # HELP instruction or 208
                readme = ReadmeInteracter.display_readme()
                print(readme)
                break
            else:
                raise ValueError(f"Unknown instruction {instruction} at position {self.program}")
        return self.stack