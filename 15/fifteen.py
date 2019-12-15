import random
import copy

def load(file):
    with open(file, 'r') as file:
        return [int(x) for x in file.read().strip().split(',')]


#  -------- Intcode

class Intcode:
    ari_ins_len = 4
    jump_ins_len = 3
    io_ins_len = 2

    def __init__(self, code: []):
        self.code = code.copy() + [0]
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

north = 1
south = 2
west = 3
east = 4

wall = 0
open_space = 1
oxygen_system = 2
oxygen = 3


def move(pos, dir):
    if dir == north:
        return pos[0], pos[1] - 1
    if dir == south:
        return pos[0], pos[1] + 1
    if dir == west:
        return pos[0] - 1, pos[1]
    if dir == east:
        return pos[0] + 1, pos[1]
    raise Exception("Bleeh!")


def get_dir(from_pos, to_pos):
    if from_pos[0] < to_pos[0]:
        return east
    if from_pos[0] > to_pos[0]:
        return west
    if from_pos[1] < to_pos[1]:
        return south
    if from_pos[1] > to_pos[1]:
        return north
    raise Exception("WAT!1!!")


def to_symbol(status, pos):
    if pos == (0, 0):
        return 'S'
    return {
        wall: '#',
        open_space: '.',
        oxygen_system: 'X',
        oxygen: 'O'
    }[status]


def print_map(explored_map):
    xs = [c[0] for c in explored_map.keys()]
    minx = min(xs)
    maxx = max(xs)
    ys = [c[1] for c in explored_map.keys()]
    miny = min(ys)
    maxy = max(ys)
    print("Map:")
    for y in range(miny, maxy + 1):
        print(''.join([to_symbol(explored_map[(x, y)], (x, y)) if (x, y) in explored_map else ' ' for x in range(minx, maxx + 1)]))


def get_possible_positions(explored_map, current_pos):
    possibles = [(move(current_pos, d), d) for d in range(1, 5)]
    return [p for p in possibles if p[0] not in explored_map or explored_map[p[0]] != wall]


def next_unexplored_dir(explored_map, current_pos):
    possibles = [(move(current_pos, d), d) for d in range(1, 5)]
    possibles = [p for p in possibles if p[0] not in explored_map]
    if len(possibles) == 0:
        return None
    # Shake it up
    random.shuffle(possibles)
    return possibles[0][1]


def next_dir(explored_map, current_pos):
    possibles = get_possible_positions(explored_map, current_pos)
    # Shake it up
    random.shuffle(possibles)
    for possible_pos, dir in possibles:
        if possible_pos not in explored_map:
            #print(f"Picked an unexplored pos {possible_pos} dir {dir}")
            return dir
    # Shake it up some more
    random.shuffle(possibles)
    for possible_pos, dir in possibles:
        if explored_map[possible_pos] == open_space:
            #print(f"Picked an already explored pos {possible_pos} dir {dir}")
            return dir
    raise Exception("You don't have a clue!")


def explore(intcode, explored_map):
    print("Exploring...")
    current_pos = (0, 0)
    current_dir = north
    explored_map[current_pos] = open_space
    while not intcode.finished:
        output = intcode.run(current_dir, 1)[0]
        #print(f"Out {output}, pos {current_pos}, dir {current_dir}")
        explored_map[move(current_pos, current_dir)] = output
        if output == wall:
            current_dir = next_dir(explored_map, current_pos)
        elif output == open_space:
            current_pos = move(current_pos, current_dir)
            # Have we been to the next place?
            if move(current_pos, current_dir) in explored_map:
                current_dir = next_dir(explored_map, current_pos)
        elif output == oxygen_system:
            current_pos = move(current_pos, current_dir)
            break  # All done here
        #print_map(explored_map)
    return current_pos


# Inspired by https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
def astar(intcode, explored_map, start_pos, goal=(0, 0)):
    print(f"Finding the way from {start_pos} to {goal}")
    open_list = [start_pos + (0, 0, 0, None, None, copy.deepcopy(intcode))]
    g = 2
    h = 3
    f = 4
    code_pos = 7
    closed_set = {}
    while len(open_list) > 0:
        open_list = sorted(open_list, key=lambda x: x[f])
        current_node = open_list.pop(0)
        #print(f"Picked current {current_node}")
        closed_set[current_node[:2]] = current_node
        # Done here return path
        if current_node[:2] == goal:
            print("Found path...")
            path = []
            cur = current_node
            while cur[5:7] != (None, None):
                path.append(cur[:2])
                cur = closed_set[cur[5:7]]
            return path[::-1]  # From start to oxygen system
        next_nodes = []
        # Assemble next moves
        possibles = get_possible_positions(explored_map, current_node[:2])
        for p in possibles:
            # Make a actual move for the robot, and store the code position
            code = copy.deepcopy(current_node[code_pos])
            dir = p[1]
            output = code.run(dir, 1)[0]
            explored_map[p[0]] = output
            if output != wall:
                next_nodes.append(p[0] + (0, 0, 0) + current_node[:2] + tuple([code]))
        # Do the magic
        for next in next_nodes:
            if next[:2] not in closed_set:
                g_value = current_node[g] + 1
                # Manhattan distance, with goal coords (0, 0)
                h_value = abs(next[0]) + abs(next[1])
                #h_value = ((next[0] - goal[0]) ** 2) + ((next[1] - goal[1]) ** 2)
                f_value = g_value + h_value
                for o in open_list:
                    if o[:2] == next[:2] and g_value > o[g]:
                        continue
                open_list.append((next[:2] + (g_value, h_value, f_value) + next[5:]))
    return None


# Only look within the known boundries, there is a slight chance we have a "synthetic" boundry,
# but I figure the exploratory part will cross it
def find_unexplored_position(explored_map):
    xs = [c[0] for c in explored_map.keys()]
    minx = min(xs)
    maxx = max(xs)
    ys = [c[1] for c in explored_map.keys()]
    miny = min(ys)
    maxy = max(ys)
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) not in explored_map:
                return x, y
    return None


# Fully explore a already started exploration
def fully_explore(intcode, explored_map, pos):
    print("Fully exploring...")
    current_pos = pos
    current_dir = 1
    all_explored = False
    path = []
    while not all_explored and not intcode.finished:
        outputs = intcode.run(current_dir, 1)
        if not intcode.finished:
            output = outputs[0]
            if output != wall:
                current_pos = move(current_pos, current_dir)
            explored_map[move(current_pos, current_dir)] = output
            current_dir = next_unexplored_dir(explored_map, current_pos)
            if current_dir is None and len(path) == 0:
                unexplored = find_unexplored_position(explored_map)
                all_explored = unexplored is None
                if unexplored is not None:
                    path = astar(intcode, explored_map, current_pos, unexplored)
            else:
                # Walk the path
                current_dir = get_dir(current_pos, path.pop(0))
        # print_map(explored_map)
    print("Full explore done!")
    return current_pos


def oxygen_spread(explored_map, start_pos):
    current_positions = [start_pos]
    explored_map[start_pos] = oxygen
    minutes = 0
    while len(current_positions) > 0:
        next_positions = []
        for pos in current_positions:
            next_positions += [p[0] for p in get_possible_positions(explored_map, pos)]
        next_positions = list(set([n for n in next_positions if explored_map[n] != oxygen]))
        for next in next_positions:
            explored_map[next] = oxygen
        current_positions = next_positions
        if len(current_positions) > 0:
            minutes += 1
        print_map(explored_map)
    return minutes


explored_map = {}
intcode = Intcode(load('input.txt'))
oxygen_system_pos = explore(intcode, explored_map)
print(oxygen_system_pos)
print_map(explored_map)

path = astar(intcode, explored_map, oxygen_system_pos)
print(path)
print(f"Part one: smallest nr of moves {len(path) if path else 'ERROR'}")

fully_explore(intcode, explored_map, oxygen_system_pos)
print_map(explored_map)
minutes = oxygen_spread(explored_map, oxygen_system_pos)
print(f"Part two: {minutes} minutes")
