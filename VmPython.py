class SimpleVM:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.program_counter = 0

    def execute(self, bytecode):
        while self.program_counter < len(bytecode):
            instruction = bytecode[self.program_counter]
            # Implement logic for different opcodes (e.g., PUSH, ADD, STORE, LOAD)
            if instruction == "PUSH":
                value = bytecode[self.program_counter + 1]
                self.stack.append(value)
                self.program_counter += 2
            elif instruction == "ADD":
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                self.stack.append(operand1 + operand2)
                self.program_counter += 1
            # ... other instructions
            else:
                raise ValueError(f"Unknown instruction: {instruction}")

# Example bytecode (simplified)
bytecode = ["PUSH", 5, "PUSH", 3, "ADD"]

vm = SimpleVM()
vm.execute(bytecode)
print(vm.stack) # Output: [8]