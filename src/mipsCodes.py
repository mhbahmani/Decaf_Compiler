debug = True
lable_count = 0

def create_lable():
    out = "_l" + str(lable_count)
    lable_count += 1
    return out


def emit_comment(comment):
    if debug:
        print("#" + comment)


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
    print("jalr", register)

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