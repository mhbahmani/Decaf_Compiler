debug = True
lable_count = 0

def create_lable():
    global lable_count
    out = "_l" + str(lable_count)
    lable_count += 1
    return out


def emit_comment(comment):
    if debug:
        print("# " + comment)


def emit(line):
    print(line)


def emit_lable(lable):
    print(lable + " :")


def emit_add(output, input1, input2):
    print("add " + output + ", " + input1 + ", " + input2)


def emit_addi(output, input1, imediete):
    print("addi " + output + ", " + input1 + ", " + imediete)


def emit_syscal():
    print("syscall")


def emit_jal(lable):
    print("jal " + lable)

def emit_j(lable):
    print("j " + lable)


def emit_jalr(register):
    print("jalr " + register)


def emit_jr():
    print("jr $ra")


def emit_branch_zero(check, lable):
    print("beqz " + check + ", " + lable)

def emit_move(destination, source):
    print("move " + destination + ", " + source)


def emit_la(destination, lable):
    print("la " + destination + ", " + lable)


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

def add_data(lable, definition):
    global data_section
    data_section += lable + " :\n" + definition


def print_data_section():
    global data_section
    print(data_section)


def push_stack(source):
    emit_addi("$sp", "$sp", "-4")
    emit_sw(source, "sp")

def emit_sw(source, destinaton, offset = 0):
    print("sw " + source + ", " + str(offset) + "(" + destinaton + ")")



def emit_itob():
    emit_lable("___itob")
    emit_lw("$s0", "$fp", 4)
    emit_li("$v0", "0")
    emit_branch_zero("$s0", "___itob_ret")
    emit_li("$v0", "1")
    emit_lable("___itob_ret")
    emit_jr()
    

def emit_btoi():
    emit_lable("___btoi")
    emit_lw("$v0", "$fp", 4)
    emit_jr()
