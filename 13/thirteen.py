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
        self.outputs = []
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

    def run(self, input: int, output_batch: int) -> []:
        inputs = [input]
        input_index = 0
        self.outputs = []
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
                self.outputs.append(self.get_value(section[1], modes[0]))
                # print(f"Outputs {self.outputs}")
                self.ptr += self.io_ins_len

                if len(self.outputs) == output_batch:
                    break  # Break for processing of output

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
        return self.outputs


#  -------- Intcode

def get_input(pad, ball):
    if pad and ball:
        if ball[0] < pad[0]:
            return -1
        elif ball[0] > pad[0]:
            return 1
    return 0


def game(code):
    intcode = Intcode(code)
    frame = {}
    score = 0
    input = 0
    pad_pos = None
    ball_pos = None
    while not intcode.finished:
        instructions = intcode.run(input, 3)
        if not intcode.finished:
            coord = instructions[0], instructions[1]
            if coord == (-1, 0):
                score = instructions[2]
                #print(f"Score: {score}")
            else:
                tile = instructions[2]
                frame[coord] = tile

                if tile == 3:
                    pad_pos = coord
                elif tile == 4:
                    ball_pos = coord
                input = get_input(pad_pos, ball_pos)

            #print_frame(frame)
    return frame, score


def display(tile):
    if tile == 0:
        return ' '
    if tile == 1:
        return 'X'
    if tile == 2:
        return u"\u2588"
    if tile == 3:
        return '_'
    if tile == 4:
        return '*'
    raise Exception(f"Unknown tile {tile}")


def print_frame(frame):
    xs = [c[0] for c in frame.keys()]
    ys = [c[1] for c in frame.keys()]
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)
    for y in range(miny, maxy + 1):
        row = []
        for x in range(minx, maxx + 1):
            if (x, y) in frame:
                row.append(display(frame[(x, y)]))
            else:
                row.append(' ')
        print(''.join(row))


frame, _ = game(load('input.txt'))
print_frame(frame)
print(f"Part one: {len([x for x in frame.values() if x == 2])} blocks")

code = load('input.txt')
code[0] = 2  # Free play
frame, score = game(code)

print_frame(frame)
print(f"Part two: final score {score}")
