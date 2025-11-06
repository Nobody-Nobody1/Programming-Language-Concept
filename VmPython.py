class SimpleVM:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.program_counter = 0

    def execute(self, bytecode):
        while self.program_counter < len(bytecode):
            instruction = bytecode[self.program_counter]
            # Implement logic for different opcodes (e.g., PUSH, ADD, SUBTRACT)
            if instruction == "PUSH":
                value = bytecode[self.program_counter + 1]
                self.stack.append(value)
                self.program_counter += 2
            elif instruction == "ADD":
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                self.stack.append(operand1 + operand2)
                self.program_counter += 1
            elif instruction == "SUBTRACT":
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                self.stack.append(operand1 - operand2)
                self.program_counter += 1
            elif instruction == "DIVIDE":
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                if operand2 == 0:
                    raise ZeroDivisionError("Division by zero")
                self.stack.append(operand1 // operand2)
                self.program_counter += 1
            elif instruction == "MULTIPLY":
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                self.stack.append(operand1 * operand2)
                self.program_counter += 1
            elif instruction == "PRINT":
                value = self.stack.pop()
                print(value)
                self.program_counter += 1
            
            else:
                raise ValueError(f"Unknown instruction: {instruction}")