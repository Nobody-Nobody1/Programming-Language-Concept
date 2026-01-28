from ByteCodeReader import Reader

bytecode = Reader.read_file_lines('ByteCode.txt') #used for reading bytecode file
output = Reader.find_in_nested_list(bytecode) #used for listing positions of values in bytecode

class Commands:
    #done
    ADDITION = 'ADDITION' #normal operation using numeric values
    ADDITION_REGISTER = 'ADDITION_REGISTER' #operation using values from registers
    #done
    SUBTRACT = 'SUBTRACT' #normal operation using numeric values
    SUBTRACT_REGISTER = 'SUBTRACT_REGISTER' #operation using values from registers
    #done
    MULTIPLY = 'MULIPLY' #normal operation using numeric values
    MULTIPLY_REGISTER = 'MULTIPLY_REGISTER' #operation using values from registers
    #done
    DIVIDE = 'DIVIDE' #normal operation using numeric values
    DIVIDE_REGISTER = 'DIVIDE_REGISTER' #operation using values from registers
    #done
    COMPARE = 'COMPARE' #comparison operation using numeric values
    COMPARE_REGISTER = 'COMPARE_REGISTER' #comparison operation using registers
    #done
    LOGICAL_OPERATIONS = 'LOGICAL_OPERATION' #logical operations AND, OR, NOT, XOR using values from registers
    #done
    STORE = 'STORE' #stores value in register
    #done unless more parameters needed
    PRINT = 'PRINT' #print value or use parameters to print preset values for output and debugging
    #done
    COMMENT = 'COMMENT' #ignores the line as comment
    #done
    MARK = 'MARK' #marks a position in the code
#adding loops such as if while and for
class VMPython:
    def execute():

        Registers = {'CompareFlag': 0, 'LOGIC_FLAG': False}  # Initialize flags for usage
        Markers = {}  # To store marked positions for jumps

        for instruction in bytecode:

            instruction_name = instruction[0].upper()
               
            if instruction_name == Commands.ADDITION:  # Addition operations
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                register = instruction[3]
                register_value = value1 + value2
                Registers.update({register: register_value})
            
            elif instruction_name == Commands.ADDITION_REGISTER: # Addition operations using registers
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                register = instruction[3]
                register_value = value1 + value2
                Registers.update({register: register_value})

            
                
            elif instruction_name == Commands.SUBTRACT: #subtraction operations
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                register = instruction[3]
                register_value = value1 - value2
                Registers.update({register: register_value})

            elif instruction_name == Commands.SUBTRACT_REGISTER: #subtraction operations using registers
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                register = instruction[3]
                register_value = value1 - value2
                Registers.update({register: register_value})


                
            elif instruction_name == Commands.MULTIPLY: #multiplication operations
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                register = instruction[3]
                register_value = value1 * value2
                Registers.update({register: register_value})
            
            elif instruction_name == Commands.MULTIPLY_REGISTER: #multiplication operations using registers
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                register = instruction[3]
                register_value = value1 * value2
                Registers.update({register: register_value})


                
            elif instruction_name == Commands.DIVIDE: #division operations
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                if value2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                register = instruction[3]
                register_value = value1 / value2
                Registers.update({register: register_value})
            
            elif instruction_name == Commands.DIVIDE_REGISTER: #division operations using registers
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                if value2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                register = instruction[3]
                register_value = value1 / value2
                Registers.update({register: register_value})


            
            elif instruction_name == Commands.COMPARE: #comparison operation
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                register = 'CompareFlag'
                comparison_parameter = int(instruction[3]) #0 equal, 1 greater, 2 less
                if comparison_parameter == 0:
                    if value1 == value2: #0 for equal
                        Registers.update({register: 1})
                    else:
                        Registers.update({register: 0})
                elif comparison_parameter == 1: #1 for greater
                    if value1 > value2:
                        Registers.update({register: 1})
                    else:
                        Registers.update({register: 0})
                elif comparison_parameter == 2: #2 for less
                    if value1 < value2:
                        Registers.update({register: 1})
                    else:
                        Registers.update({register: 0})
                
            elif instruction_name == Commands.COMPARE_REGISTER: #comparison operation using registers
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                register = 'CompareFlag'
                comparison_parameter = int(instruction[3]) #0 equal, 1 greater, 2 less
                if comparison_parameter == 0:
                    if value1 == value2: #0 for equal
                        Registers.update({register: 1})
                    else:
                        Registers.update({register: 0})
                elif comparison_parameter == 1: #1 for greater
                    if value1 > value2:
                        Registers.update({register: 1})
                    else:
                        Registers.update({register: 0})
                elif comparison_parameter == 2: #2 for less
                    if value1 < value2:
                        Registers.update({register: 1})
                    else:
                        Registers.update({register: 0})



            elif instruction_name == Commands.LOGICAL_OPERATIONS: #logical operations
                operation = instruction[1].upper()  # logical operation type
                value0 = Registers.get(instruction[2])
                value1 = Reader.string_to_bool(value0) #prepares first value
                value2 = Registers.get(instruction[3]) 
                value3 = Reader.string_to_bool(value2) #prepares second value
                register = 'LOGIC_FLAG'
                if operation == 'AND':
                    result = value1 and value3
                    Registers.update({register: result})
                elif operation == 'OR':
                    result = value1 or value3
                    Registers.update({register: result})
                elif operation == 'XOR':
                    result = value1 ^ value3
                    Registers.update({register: result})
                elif operation == 'NOT':
                    result = not value1
                    Registers.update({register: result})



            elif instruction_name == Commands.STORE: #stores value in register
                register = instruction[1]
                value = instruction[2]
                if value in Registers: #checks if the value is in registers
                    value = Registers[value]
                Registers.update({register: value})
            


            elif instruction_name == Commands.PRINT:
                value = instruction[1]
                if value == 'registers_debug': #checks for special print command
                    print(Registers)
                elif value == 'markers_debug':
                    print(Markers)
                elif value == 'bytecode_debug':
                    print(bytecode)
                elif value == 'output_debug':
                    print(output)
                elif value in Registers: #checks if the value is in registers
                    value = Registers[value]



            elif instruction_name == Commands.COMMENT:
                continue  # Ignore comments
                
        
        
            elif instruction_name == Commands.MARK:
                marker_name = instruction[1]
                current_position = bytecode.index(instruction) + 1
                Markers.update({marker_name: current_position})