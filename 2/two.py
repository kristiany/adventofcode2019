with open('input.txt', 'r') as file:
    code = [int(x) for x in file.read().strip().split(',')]


def run(program: []) -> []:
    code = program.copy()
    i = 0
    while i < len(code):
        value = code[i]
        if value == 99:
            #print("Program finished OK, exiting")
            break
        elif value == 1:
            v1 = code[code[i + 1]]
            v2 = code[code[i + 2]]
            pos = code[i + 3]
            result = v1 + v2
            code[pos] = result
            #print(f"add {v1} + {v2} = {result} at position {pos}")
            i += 4
        elif value == 2:
            v1 = code[code[i + 1]]
            v2 = code[code[i + 2]]
            pos = code[i + 3]
            result = v1 * v2
            code[pos] = result
            #print(f"mul {v1} * {v2} = {result} at position {pos}")
            i += 4
        else:
            raise Exception(f"Unexpected op {value}")
    return code


code[1] = 12
code[2] = 2
print(f"Part one: {run(code)[0]}")

for noun in range(0, 100):
    for verb in range(0, 100):
        code[1] = noun
        code[2] = verb
        if run(code)[0] == 19690720:
            print(f"Part two: Found noun={noun}, verb={verb} yields 19690720: answer = {100 * noun + verb}")
            exit(0)

print("Found nothing")