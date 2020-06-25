import sys
import re

symbol_table = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SCREEN": "16384",
    "KBD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4"
}

inFile = sys.argv[1]
outFile = f'{sys.argv[1][0:-4]}.hack'

# parser module

def is_instruction(line):
    if line[0] == "/" or line == '\n':
        return False
    else:
        return True

def is_A_instruction(line):
    if line[0] == "@":
        return True
    else:
        return False

def is_label_declaration(line):
    if line[0] == "(":
        return True
    else:
        return False

def extract_label_symbol(line):
    right_bracket = line.find(")")

    label = line[1: right_bracket]

    return label

def parse_C_instruction(line):
    if line.find("//") > -1:
        right_index = line.find("//")
    else:
        right_index = len(line)

    dest_index = line.find("=")
    comp_index = line.find(";")

    if dest_index > 0:
        dest = line[:dest_index]
    else:
        dest = None

    if comp_index > 0:
        comp = line[dest_index + 1: comp_index]
        jump = line[comp_index + 1:right_index]
    else:
        comp = line[dest_index + 1:right_index]
        jump = None

    return dest, comp, jump 

# code module

def translate_A_instruction(line):
    # get integer value
    int_string = line[1:]
    int_value = int(int_string)

    # translate to binary string
    binary_string = ["0" for i in range(15)]
    for index, digit in enumerate(binary_string):
        place_value = 2**(14-index)
        if int_value // place_value == 1:
            binary_string[index] = "1" 
            int_value = int_value - place_value
                
    # output to file
    binary_string = ''.join(binary_string)
    binary_string = "0" + binary_string
    return binary_string

def resolve_A_instruction(line, n):
    if line.find("//") > -1:
        right_index = line.find("//")
        symbol = line[1:right_index]
    else:
        symbol = line[1:]

    if symbol in symbol_table.keys():
        resolved_line = "@" + symbol_table[symbol]
    elif is_non_negative_int(symbol):
        resolved_line = "@" + symbol
    else:
        # is variable and add to table
        symbol_table[symbol] = str(n)
        resolved_line = "@" + str(n)
        n = n + 1

    return resolved_line, n

def translate_C_instruction(dest, comp, jump):
    # initialize lists for codes
    dest_code = ["0" for i in range(3)]
    comp_code = ["0" for i in range(7)]

    if dest:
        if "A" in dest:
            dest_code[0] = "1"
        if "D" in dest:
            dest_code[1] = "1"
        if "M" in dest:
            dest_code[2] = "1"
        dest_code = "".join(dest_code)
    else:
        dest_code = "000"

    # logic for comp_code
    if "M" in comp:
        comp_code[0] = "1"

    if comp == "0":
        comp_code[1] = "1"
        comp_code[3] = "1"
        comp_code[5] = "1"
    elif comp == "1":
        comp_code[1] = "1"
        comp_code[2] = "1"
        comp_code[3] = "1"
        comp_code[4] = "1"
        comp_code[5] = "1"
        comp_code[6] = "1"
    elif comp == "-1":
        comp_code[1] = "1"
        comp_code[2] = "1"
        comp_code[3] = "1"
        comp_code[5] = "1"
    elif comp == "D":
        comp_code[3] = "1"
        comp_code[4] = "1"
    elif comp == "A" or comp == "M":
        comp_code[1] = "1"
        comp_code[2] = "1"
    elif comp == "!D":
        comp_code[3] = "1"
        comp_code[4] = "1"
        comp_code[6] = "1"
    elif comp == "!A" or comp == "!M":
        comp_code[1] = "1"
        comp_code[2] = "1"
        comp_code[6] = "1"
    elif comp == "-D":
        comp_code[3] = "1"
        comp_code[4] = "1"
        comp_code[5] = "1"
        comp_code[6] = "1"
    elif comp == "-A" or comp == "-M":
        comp_code[1] = "1"
        comp_code[2] = "1"
        comp_code[5] = "1"
        comp_code[6] = "1"
    elif comp == "D+1":
        comp_code[2] = "1"
        comp_code[3] = "1"
        comp_code[4] = "1"
        comp_code[5] = "1"
        comp_code[6] = "1"
    elif comp == "A+1" or comp == "M+1":
        comp_code[1] = "1"
        comp_code[2] = "1"
        comp_code[4] = "1"
        comp_code[5] = "1"
        comp_code[6] = "1"
    elif comp == "D-1":
        comp_code[3] = "1"
        comp_code[4] = "1"
        comp_code[5] = "1"
    elif comp == "A-1" or comp == "M-1":
        comp_code[1] = "1"
        comp_code[2] = "1"
        comp_code[5] = "1"
    elif comp == "D+A" or comp == "D+M":
        comp_code[5] = "1"
    elif comp == "D-A" or comp == "D-M":
        comp_code[2] = "1"
        comp_code[5] = "1"
        comp_code[6] = "1"
    elif comp == "A-D" or comp == "M-D":
        comp_code[4] = "1"
        comp_code[5] = "1"
        comp_code[6] = "1"
    elif "|" in comp:
        comp_code[2] = "1"
        comp_code[4] = "1"
        comp_code[6] = "1"
    # D&A and M&A strings are all zero which is default

    comp_code = "".join(comp_code)

    if jump:
        if jump == "JGT":
            jump_code = "001"
        elif jump == "JEQ":
            jump_code = "010"
        elif jump == "JGE":
            jump_code = "011"
        elif jump == "JLT":
            jump_code = "100"
        elif jump == "JNE":
            jump_code = "101"
        elif jump == "JLE":
            jump_code = "110"
        else:
            jump_code = "111"
    else:
        jump_code = "000"

    op_code = "111"

    string = op_code + comp_code + dest_code + jump_code

    return string
  
# utilities

def is_non_negative_int(string):
    regex = r'[\WA-Za-z_]'
    match = re.search(regex, string)
    if match:
        return False
    else:
        return True

# main program

with open(inFile, 'r') as inf, open(outFile, 'w') as outf:

    n = 0
    # first pass for labels
    for line in inf:
        if is_instruction(line):
            if is_label_declaration(line):
                label = extract_label_symbol(line)
                symbol_table[label] = str(n)
            else:
                n = n+1

    inf.seek(0)

    n = 16
    # second pass
    for line in inf:
        if is_instruction(line):

            line_stripped = "".join(line.split())

            if is_A_instruction(line_stripped):
                resolved_instruction, n = resolve_A_instruction(line_stripped, n)
                binary_string = translate_A_instruction(resolved_instruction)
                outf.write(binary_string)
                outf.write('\n')

            elif not is_label_declaration(line_stripped):
                dest, comp, jump = parse_C_instruction(line_stripped)
                c_in = translate_C_instruction(dest, comp, jump)
                outf.write(c_in)
                outf.write('\n')