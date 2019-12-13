from math import gcd

def load(file):
    with open(file, 'r') as file:
        return file.read().strip().split('\n')


class C:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def add(self, c):
        self.x += c.x
        self.y += c.y
        self.z += c.z

    def sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Moon:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    @staticmethod
    def velocity(c1, c2):
        if c1 < c2:
            return 1
        if c1 > c2:
            return -1
        return 0

    def calc_velocity(self, other):
        self.vel.add(C(
            self.velocity(self.pos.x, other.pos.x),
            self.velocity(self.pos.y, other.pos.y),
            self.velocity(self.pos.z, other.pos.z)))

    def total_energy(self):
        return self.pos.sum() * self.vel.sum()


def read_moons(filename):
    moons_inputs = load(filename)
    moons = []
    for moon_input in moons_inputs:
        cs = moon_input.split(',')
        moons.append(Moon(
            C(
                int(cs[0].split('=')[1].replace('>', '')),
                int(cs[1].split('=')[1].replace('>', '')),
                int(cs[2].split('=')[1].replace('>', ''))
            ),
            C()))
    return moons


def print_moons(moons):
    for moon in moons:
        print(f"pos: ({moon.pos.x}, {moon.pos.y}, {moon.pos.z}), vel: ({moon.vel.x}, {moon.vel.y}, {moon.vel.z})")


def moon_step(moons):
    for i, moon in enumerate(moons):
        for other in moons[i + 1:]:
            moon.calc_velocity(other)
            other.calc_velocity(moon)

    for moon in moons:
        moon.pos.add(moon.vel)


moons = read_moons('input.txt')
#print_moons(moons)
for k in range(0, 1000):
    moon_step(moons)
    #print(k)
    #print_moons(moons)

print(f"Part one: total energy {sum([m.total_energy() for m in moons])}")

moons = read_moons('input.txt')
x_axis = [m.pos.x for m in moons]
y_axis = [m.pos.y for m in moons]
z_axis = [m.pos.z for m in moons]
zeros = [0] * 4
x_step = None
y_step = None
z_step = None
k = 1
while not x_step or not y_step or not z_step:
    moon_step(moons)

    if not x_step and x_axis == [m.pos.x for m in moons] and zeros == [m.vel.x for m in moons]:
        print(f"x {k}:{moons[0].pos.x}\t{moons[1].pos.x}\t{moons[2].pos.x}\t{moons[0].pos.x}")
        x_step = k
    if not y_step and y_axis == [m.pos.y for m in moons] and zeros == [m.vel.y for m in moons]:
        print(f"y {k}:{moons[0].pos.y}\t{moons[1].pos.y}\t{moons[2].pos.y}\t{moons[0].pos.y}")
        y_step = k
    if not z_step and z_axis == [m.pos.z for m in moons] and zeros == [m.vel.z for m in moons]:
        print(f"z {k}:{moons[0].pos.z}\t{moons[1].pos.z}\t{moons[2].pos.z}\t{moons[0].pos.z}")
        z_step = k

    k += 1


# Borrowed from https://gist.github.com/endolith/114336/eff2dc13535f139d0d6a2db68597fad2826b53c3
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return int(a * b / gcd(a, b))


print(f"Steps x {x_step}, y {y_step}, z {z_step}")
max_step = lcm(lcm(x_step, y_step), z_step)
print(f"Part two: {max_step}")


