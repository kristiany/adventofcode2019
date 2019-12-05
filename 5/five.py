ari_ins_len = 4
jump_ins_len = 3
io_ins_len = 2


with open('input.txt', 'r') as file:
    code = [int(x) for x in file.read().strip().split(',')]

def get_modes(section):
    modes = list(str(section[0]))
    modes = modes[0: len(modes) - 2]  # Trim down
    while len(modes) < 3:  # Pad
        modes.insert(0, '0')
    #print(f"Modes: {modes}")
    return list(reversed(modes))


def get_value(code, value, mode):
    if mode == '1':
        return value
    return code[value]


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def op(code, section, func):
    modes = get_modes(section)
    v1 = get_value(code, section[1], modes[0])
    v2 = get_value(code, section[2], modes[1])
    result = func(v1, v2)
    pos = section[3]
    code[pos] = result
    #print(f"{func} {v1}, {v2} = {result} at position {pos}")


def run(program: [], input) -> []:
    code = program.copy()
    i = 0
    output = None
    while i < len(code):
        value = code[i]
        instruction = str(value)[::-1][0]
        if value == 99:
            print("Program finished OK, exiting")
            break
        elif instruction == '1':
            op(code, code[i: i + ari_ins_len], add)
            i += ari_ins_len
        elif instruction == '2':
            op(code, code[i: i + ari_ins_len], mul)
            i += ari_ins_len
        elif instruction == '3':
            code[code[i + 1]] = input
            i += io_ins_len
        elif instruction == '4':
            section = code[i: i + io_ins_len]
            modes = get_modes(section)
            output = get_value(code, section[1], modes[0])
            print(f"Output {output}")
            i += io_ins_len
        elif instruction == '5':
            section = code[i: i + jump_ins_len]
            modes = get_modes(section)
            if get_value(code, section[1], modes[0]) == 0:
                i += jump_ins_len
            else:
                i = get_value(code, section[2], modes[1])
        elif instruction == '6':
            section = code[i: i + jump_ins_len]
            modes = get_modes(section)
            if get_value(code, section[1], modes[0]) == 0:
                i = get_value(code, section[2], modes[1])
            else:
                i += jump_ins_len
        elif instruction == '7':
            section = code[i: i + ari_ins_len]
            modes = get_modes(section)
            if get_value(code, section[1], modes[0]) < get_value(code, section[2], modes[1]):
                code[section[3]] = 1
            else:
                code[section[3]] = 0
            i += ari_ins_len
        elif instruction == '8':
            section = code[i: i + ari_ins_len]
            modes = get_modes(section)
            if get_value(code, section[1], modes[0]) == get_value(code, section[2], modes[1]):
                code[section[3]] = 1
            else:
                code[section[3]] = 0
            i += ari_ins_len
        else:
            raise Exception(f"Unexpected op {value}")
    return output


print(f"Part one: {run(code, 1)}")

# --------------- TEST -------------------
tests = [
    ('3,9,8,9,10,9,4,9,99,-1,8', 3, 0, 8, 1),
    ('3,9,7,9,10,9,4,9,99,-1,8', 11, 0, 7, 1),
    ('3,3,1108,-1,8,3,4,3,99', 5, 0, 8, 1),
    ('3,3,1107,-1,8,3,4,3,99', 10, 0, 7, 1),
    ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 0, 0, 8, 1),
    ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 0, 0, 3, 1),
]
for test in tests:
    test_code = [int(x) for x in test[0].split(',')]
    run1 = run(test_code, test[1])
    if run1 != test[2]:
        raise Exception(f"Error for test case {test}, {run1} != {test[2]}")
    run2 = run(test_code, test[3])
    if run2 != test[4]:
        raise Exception(f"Error for test case {test}, {run2} != {test[4]}")

with open('test.txt', 'r') as file:
    test_code = [int(x) for x in file.read().strip().split(',')]

assert run(test_code, 7) == 999
assert run(test_code, 8) == 1000
assert run(test_code, 11) == 1001

# -----------------------------------------
print(f"Part two: {run(code, 5)}")

