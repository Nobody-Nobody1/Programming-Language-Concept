class SimpleVM:
    def __init__(self):
        self.stack = [] #stack for calculations
        self.memory = {} #memory for storage
        self.program_counter = 0 #counts current instruction

    def execute(self, bytecode):
        while self.program_counter < len(bytecode):
            instruction = bytecode[self.program_counter]
            
            if instruction == "PUSH": #adds next value to stack
                value = bytecode[self.program_counter + 1]
                self.stack.append(value)
                self.program_counter += 2
            elif instruction == "ADD": #adds top two values on stack
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                self.stack.append(operand1 + operand2)
                self.program_counter += 1
            elif instruction == "SUBTRACT": #subtracts top two values on stack
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                self.stack.append(operand1 - operand2)
                self.program_counter += 1
            elif instruction == "DIVIDE": #divides top two values on stack
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                if operand2 == 0:
                    raise ZeroDivisionError("Division by zero")
                self.stack.append(operand1 // operand2)
                self.program_counter += 1
            elif instruction == "MULTIPLY": #multiplies top two values on stack
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                self.stack.append(operand1 * operand2)
                self.program_counter += 1
            elif instruction == "MEM_DEBUG" : #prints current memory state
                print(self.memory)
                self.program_counter += 1
            elif instruction == "COMMENT": #ignores comments
                self.program_counter += 2
            elif instruction == "PRINT": #prints top of stack
                value = self.stack
                print(value)
                self.program_counter += 1
            elif instruction == "HALT": #stops execution
                break
            elif instruction == "INPUT": #takes user input and pushes to stack
                user_input = int(input("Enter an integer: "))
                self.stack.append(user_input)
                self.program_counter += 1
            else:
                raise ValueError(f"Unknown instruction: {instruction}")