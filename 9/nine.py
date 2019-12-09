def load(file):
    with open(file, 'r') as file:
        return [int(x) for x in file.read().strip().split(',')]

#  -------- Intcode

class Intcode:
    ari_ins_len = 4
    jump_ins_len = 3
    io_ins_len = 2

    def __init__(self, code: [], extended_size=1000):
        self.code = code.copy() + [0] * extended_size
        self.ptr = 0
        self.relative_base = 0
        self.finished = False
        self.output = None
        self.extension = {}

    def get_modes(self, section):
        modes = list(str(section[0]))
        modes = modes[0: len(modes) - 2]  # Trim down
        while len(modes) < 3:  # Pad
            modes.insert(0, '0')
        return list(reversed(modes))

    def get_value(self, value, mode):
        if mode == '1':
            return value
        if mode == '2':
            index = value + self.relative_base
            if index >= len(self.code):
                return self.extension[index]
            else:
                return self.code[index]

        if value >= len(self.code):
            print(f"Indexing out of range: {value}/{len(self.code)}")

        if value >= len(self.code):
            return self.extension[value]
        return self.code[value]

    def get_index(self, value, mode):
        if mode == '2':
            return value + self.relative_base
        return value

    @staticmethod
    def add(x: int, y: int):
        return x + y

    @staticmethod
    def mul(x: int, y: int):
        return x * y

    def op(self, size, func):
        section, modes = self.block(size)
        v1 = self.get_value(section[1], modes[0])
        v2 = self.get_value(section[2], modes[1])
        result = func(v1, v2)
        pos = self.get_index(section[3], modes[2])
        if pos >= len(self.code):
            self.extension[pos] = result
        else:
            self.code[pos] = result

    def block(self, size):
        section = self.code[self.ptr: self.ptr + size]
        modes = self.get_modes(section)
        return section, modes

    def run(self, input: int) -> []:
        inputs = [input]
        input_index = 0
        while self.ptr < len(self.code):
            value = self.code[self.ptr]
            instruction = str(value)[::-1][0]
            if value == 99:
                print("Program finished OK, exiting")
                self.finished = True
                break
            elif instruction == '1':
                self.op(self.ari_ins_len, Intcode.add)
                self.ptr += self.ari_ins_len
            elif instruction == '2':
                self.op(self.ari_ins_len, Intcode.mul)
                self.ptr += self.ari_ins_len
            elif instruction == '3':
                section, modes = self.block(self.io_ins_len)
                insert_index = self.get_index(section[1], modes[0])
                if insert_index >= len(self.code):
                    self.extension[insert_index] = inputs[input_index]
                else:
                    self.code[insert_index] = inputs[input_index]
                input_index += 1
                self.ptr += self.io_ins_len
            elif instruction == '4':
                section, modes = self.block(self.io_ins_len)
                self.output = self.get_value(section[1], modes[0])
                print(f"Output {self.output}")
                self.ptr += self.io_ins_len
            elif instruction == '5':
                section, modes = self.block(self.jump_ins_len)
                if self.get_value(section[1], modes[0]) == 0:
                    self.ptr += self.jump_ins_len
                else:
                    self.ptr = self.get_value(section[2], modes[1])
            elif instruction == '6':
                section, modes = self.block(self.jump_ins_len)
                if self.get_value(section[1], modes[0]) == 0:
                    self.ptr = self.get_value(section[2], modes[1])
                else:
                    self.ptr += self.jump_ins_len
            elif instruction == '7':
                section, modes = self.block(self.ari_ins_len)
                flag_index = self.get_index(section[3], modes[2])
                flag = 1 if self.get_value(section[1], modes[0]) < self.get_value(section[2], modes[1]) else 0
                if flag_index >= len(self.code):
                    self.extension[flag_index] = flag
                else:
                    self.code[flag_index] = flag
                self.ptr += self.ari_ins_len
            elif instruction == '8':
                section, modes = self.block(self.ari_ins_len)
                flag_index = self.get_index(section[3], modes[2])
                flag = 1 if self.get_value(section[1], modes[0]) == self.get_value(section[2], modes[1]) else 0
                if flag_index >= len(self.code):
                    self.extension[flag_index] = flag
                else:
                    self.code[flag_index] = flag
                self.ptr += self.ari_ins_len
            elif instruction == '9':
                section, modes = self.block(self.io_ins_len)
                self.relative_base += self.get_value(section[1], modes[0])
                self.ptr += self.io_ins_len
            else:
                raise Exception(f"Unexpected op {value}")
        return self.output


#  -------- Intcode

#test1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
#Intcode(test1).run(0)

#test2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
#print(f"Test 2 result: {Intcode(test2).run(0)}")

#test3 = [104, 1125899906842624, 99]
#print(f"Test 3 result: {Intcode(test3).run(0)}")

print(f"Part one: keycode {Intcode(load('input.txt')).run(1)}")

print(f"Part two: coordinates {Intcode(load('input.txt')).run(2)}")