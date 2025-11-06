class TinyVM:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.program_counter = 0

    def run(self, bytecode):
        while self.program_counter < len(bytecode):
            instruction = bytecode[self.program_counter]
            opcode = instruction[0]

            if opcode == "PUSH":
                value = instruction[1]
                self.stack.append(value)
            elif opcode == "ADD":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif opcode == "PRINT":
                print(self.stack.pop())
            # ... other opcodes

            self.program_counter += 1

# Example Bytecode
bytecode = [
    ("PUSH", 5),
    ("PUSH", 10),
    ("ADD"),
    ("PRINT")
]

vm = TinyVM()
vm.run(bytecode)