import ReadmeInteracter

class SimpleVM:
    def __init__(self):
        self.stack = []
        self.instruction_pointer = 0

    def execute(self, bytecode):
        while self.instruction_pointer < len(bytecode):
            instruction = bytecode[self.instruction_pointer]

            if instruction == "PUSH":  # PUSH instruction
                self.instruction_pointer += 1
                value = bytecode[self.instruction_pointer]
                self.stack.append(value)

            elif instruction == "POP":  # POP instruction
                if self.stack:
                    self.stack.pop()
                else:
                    raise ValueError("Stack underflow in POP instruction")

            elif instruction == "ADD":  # ADD instruction
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a + b)
                else:
                    raise ValueError("Stack underflow in ADD instruction")

            elif instruction == "JUMPIFZERO":  # JUMPIFZERO instruction
                self.instruction_pointer += 1
                target = bytecode[self.instruction_pointer]
                if self.stack:
                    value = self.stack.pop()
                    if value == 0:
                        self.instruction_pointer = target - 1  # -1 to offset the upcoming increment
                else:
                    raise ValueError("Stack underflow in JUMPIFZERO instruction")
            
            elif instruction == "HELP": # HELP instruction or 208
                readme = ReadmeInteracter.display_readme()
                print(readme)
                break

            self.instruction_pointer += 1

        return self.stack