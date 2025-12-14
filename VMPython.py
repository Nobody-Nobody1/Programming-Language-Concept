import ByteCodeReader

class SimpleVM:
    def __init__(self):
        self.stack = [] #memory stack
        self.programCounter = 0 #counts instruction position

    def execute(self, bytecode):
        programCount = self.programCounter
        while programCount <= len(bytecode):
            for instr in bytecode:
                if instr == "PROGRAM_CHECK":
                    programCount += 1
                    return "program check"

                if instr == "PUSH":
                    print("hello at PUSH")
                    programCount += 1
                    
                else:
                    raise TypeError(str(instr) + " at position " + str(programCount)) #raises type error if instr unknown