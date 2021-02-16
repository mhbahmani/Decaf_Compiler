debug = True
label_count = 0

def create_lable():
    global label_count
    out = "_l" + str(label_count)
    label_count += 1
    return out


def emit_comment(comment):
    if debug:
        print("#" + comment)


def emit(line):
    print(line)


def emit_label(label):
    print(label + " :")


def emit_add(output, input1, input2):
    print("add " + output + ", " + input1 + ", " + input2)


def emit_addi(output, input1, imediete):
    print("addi " + output + ", " + input1 + ", " + imediete)


def emit_syscal():
    print("syscall")


def emit_jal(label):
    print("jal " + label)

def emit_j(label):
    print("j " + label)


def emit_jalr(register):
    print("jalr", register)


def emit_jr():
    print("jr $ra")


def emit_branch_zero(check, label):
    print("beqz " + check + ", " + label)

def emit_move(destination, source):
    print("move " + destination + ", " + source)


def emit_la(destination, label):
    print("la " + destination + ", " + label)


def emit_lw(destination, source, offset = 0, word = True):
    if word:
        print("lw " + destination + ", " + str(offset) + "(" + source + ")")
    else :
        print("lb " + destination + ", " + str(offset) + "(" + source + ")")


def emit_li(destination, imediate):
    print("li " + destination + ", " + imediate)


def emit_mult_div(register1, register2, mult = True):
    if mult:
        print("mult " + register1 + ", " + register2)
    else :
        print("div " + register1 + ", " + register2)

def emit_load_HI_LO(register, HI = True):
    if HI:
        print("mfhi " + register)
    else :
        print("mflo " + register)


data_section = '''.data
__true:
    .asciiz "true"
__false:
    .asciiz "false"
'''

def add_data(label, definition):
    global data_section
    data_section += label + " :\n" + definition


def print_data_section():
    global data_section
    print(data_section)


def push_stack(source):
    emit_addi("$sp", "$sp", "-4")
    emit_sw(source, "sp")

def emit_sw(source, destinaton, offset = 0):
    print("sw " + source + ", " + str(offset) + "(" + destinaton + ")")
