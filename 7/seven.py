import itertools


def load(file):
    with open(file, 'r') as file:
        return [int(x) for x in file.read().strip().split(',')]


#  -------- Intcode

class Amp:
    ari_ins_len = 4
    jump_ins_len = 3
    io_ins_len = 2

    def __init__(self, code: [], phase: int):
        self.code = code.copy()
        self.phase = phase
        self.ptr = 0
        self.finished = False
        self.output = None

    def get_modes(self, section):
        modes = list(str(section[0]))
        modes = modes[0: len(modes) - 2]  # Trim down
        while len(modes) < 3:  # Pad
            modes.insert(0, '0')
        return list(reversed(modes))

    def get_value(self, value, mode):
        if mode == '1':
            return value
        return self.code[value]

    @staticmethod
    def add(x: int, y: int):
        return x + y

    @staticmethod
    def mul(x: int, y: int):
        return x * y

    def op(self, section, func):
        modes = self.get_modes(section)
        v1 = self.get_value(section[1], modes[0])
        v2 = self.get_value(section[2], modes[1])
        result = func(v1, v2)
        pos = section[3]
        self.code[pos] = result

    def run(self, input: int) -> []:
        inputs = [input]
        if self.ptr == 0:
            inputs = [self.phase] + inputs
        input_index = 0
        while self.ptr < len(self.code):
            # print(f"ptr {self.ptr}: {self.code}")
            value = self.code[self.ptr]
            instruction = str(value)[::-1][0]
            if value == 99:
                #print("Program finished OK, exiting")
                self.finished = True
                break
            elif instruction == '1':
                self.op(self.code[self.ptr: self.ptr + self.ari_ins_len], Amp.add)
                self.ptr += self.ari_ins_len
            elif instruction == '2':
                self.op(self.code[self.ptr: self.ptr + self.ari_ins_len], Amp.mul)
                self.ptr += self.ari_ins_len
            elif instruction == '3':
                # print(f"{self.ptr} / {len(self.code)}, {input_index}")
                self.code[self.code[self.ptr + 1]] = inputs[input_index]
                # print(f"Input {input_index} = {inputs[input_index]}")
                input_index += 1
                self.ptr += self.io_ins_len
            elif instruction == '4':
                section = self.code[self.ptr: self.ptr + self.io_ins_len]
                modes = self.get_modes(section)
                self.output = self.get_value(section[1], modes[0])
                print(f"Output {self.output}")
                self.ptr += self.io_ins_len

                break  # Early exit

            elif instruction == '5':
                section = self.code[self.ptr: self.ptr + self.jump_ins_len]
                modes = self.get_modes(section)
                if self.get_value(section[1], modes[0]) == 0:
                    self.ptr += self.jump_ins_len
                else:
                    self.ptr = self.get_value(section[2], modes[1])
            elif instruction == '6':
                section = self.code[self.ptr: self.ptr + self.jump_ins_len]
                modes = self.get_modes(section)
                if self.get_value(section[1], modes[0]) == 0:
                    self.ptr = self.get_value(section[2], modes[1])
                else:
                    self.ptr += self.jump_ins_len
            elif instruction == '7':
                section = self.code[self.ptr: self.ptr + self.ari_ins_len]
                modes = self.get_modes(section)
                if self.get_value(section[1], modes[0]) < self.get_value(section[2], modes[1]):
                    self.code[section[3]] = 1
                else:
                    self.code[section[3]] = 0
                self.ptr += self.ari_ins_len
            elif instruction == '8':
                section = self.code[self.ptr: self.ptr + self.ari_ins_len]
                modes = self.get_modes(section)
                if self.get_value(section[1], modes[0]) == self.get_value(section[2], modes[1]):
                    self.code[section[3]] = 1
                else:
                    self.code[section[3]] = 0
                self.ptr += self.ari_ins_len
            else:
                raise Exception(f"Unexpected op {value}")
        return self.output


#  -------- Intcode

def signal(code, setting, refeed):
    data = 0
    amps = [Amp(code, p) for p in setting]
    for amp in amps:
        data = amp.run(data)
    while refeed:
        #print(f"Run with input {data}")
        for amp in amps:
            data = amp.run(data)
        if amps[4].finished:
            refeed = False
    return data


def find_max_signal(code, settings_range, refeed=False):
    max = 0
    settings = itertools.permutations(settings_range)
    for setting in settings:
        s = signal(code, setting, refeed)
        print(f"Settings {setting} produced {s}")
        if s > max:
            max = s
    return max

code = load('input.txt')
print(f"Part one: max signal {find_max_signal(code, range(5))}")

print("---------------")
test = load('test4.txt')
print(f"Part two: max signal {find_max_signal(code, range(5, 10), refeed=True)}")
