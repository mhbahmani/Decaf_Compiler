debug = True


def emit_comment(comment):
    if debug:
        emit("#" + comment)


def emit(line):
    print(line)
