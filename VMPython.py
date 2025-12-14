import ByteCodeReader

class SimpleVM:
    def __init__self(self):
        self.stack = []
    
    def execute(self, bytecode):
        for instruction in bytecode:
            parts = instruction.split()
            cmd = parts[0]
            
            if cmd == 'PUSH':
                value = int(parts[1])
                self.stack.append(value)
            elif cmd == 'POP':
                if self.stack:
                    self.stack.pop()
            elif cmd == 'ADD':
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a + b)
            elif cmd == 'SUB':
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a - b)
            # Additional instructions can be added here