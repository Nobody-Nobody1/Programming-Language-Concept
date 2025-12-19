import ByteCodeReader

class SimpleVM:
    def __init__self(self):
        self.stack = []
    
    def execute(self, bytecode):
        for instruction in bytecode:
            if instruction == "PUSH": #adds next value from bytecode to stack
                value = bytecode.pop(0)
                self.stack.append(value)
            elif instruction == "POP": #removes top value from stack
                self.stack.pop()
            elif instruction == "ADD": #adds top two values on stack
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif instruction == "MUL": #multiplies top two values on stack
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
            elif instruction == "PRINT": # prints top value of stack
                print(self.stack)
            elif instruction == "PROGRAM_CHECK": # checks if top value of stack is 0
                if self.stack[-1] == 0: # if top value is 0, program raises error
                    raise ValueError("Program check failed")
            else:
                raise ValueError(f"Unknown instruction: {instruction}") #raises error for unknown