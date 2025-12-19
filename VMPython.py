import ByteCodeReader

class SimpleVM:
    def __init__self(self):
        self.stack = []
    
    def execute(self, bytecode):
        instructions = ByteCodeReader.read(bytecode)
        if instructions is None:
            raise ValueError("Invalid bytecode")