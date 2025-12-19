import ByteCodeReader

class SimpleVM:
    def __init__(self):
        self.stack = []
        self.program = 0
    
    def execute(self, bytecode):
        for instruction in bytecode:
            if instruction == "PUSH": #adds next value from bytecode to stack
                value = bytecode[self.program + 1]
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
                print("Print :)")
            elif instruction == "PROGRAM_CHECK": # prints program check message
                print("Program Check :)")
            else:
                raise ValueError(f"Unknown instruction: {instruction}") #raises error for unknown
        else:
            return self.stack #returns final stack after execution