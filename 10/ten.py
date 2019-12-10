import math

PRECISION = 10

def load(file):
    with open(file, 'r') as file:
        return file.read().strip().split('\n')

def vector(p1, p2):
    return p2[0] - p1[0], p2[1] - p1[1]

def length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])

def normal(p1, p2):
    v = vector(p1, p2)
    m = length(v)
    return round(v[0] / m, PRECISION), round(v[1] / m, PRECISION)

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

data = load('input.txt')
asteroids = []
for y, row in enumerate(data):
    asteroids.extend([(x, y) for x, v in enumerate(row) if v == '#'])

best_loc = 0
max = 0
for i, coord in enumerate(asteroids):
    coord_normals = set()
    for other in asteroids[0:i] + asteroids[i + 1:]:
        n = normal(coord, other)
        coord_normals.add(n)
    if len(coord_normals) > max:
        max = len(coord_normals)
        best_loc = i

station = asteroids[best_loc]
print(f"Part one: max {max}, in location {station}")

ast_data = []
unit_up = 0.0, -1.0
unit_down = 0.0, 1.0
for ast in asteroids[0:best_loc] + asteroids[best_loc + 1:]:
    v = vector(station, ast)
    n = normal(station, ast)
    if n[0] < 0:
        rot = math.acos(dot(unit_down, n)) + math.pi
    else:
        rot = math.acos(dot(unit_up, n))
    ast_data.append({
        "coord": ast,
        "z": round(length(v), PRECISION),
        "rotation": round(rot, PRECISION),
        "v": v,
        "n": n
    })

grouped = []
rotations = sorted(set(map(lambda x: x['rotation'], ast_data)))
for rotation in rotations:
    z_list = sorted([x for x in ast_data if x['rotation'] == rotation], key=lambda x: (x['z']))
    grouped.append(z_list)

turn = 0
nr = 1
turning = True
order = []
while turning:
    ast_left = False
    for group in grouped:
        if turn < len(group):
            #print(f"Turn {turn}, nr {nr}: {group[turn]}")
            order.append(group[turn])
            nr += 1
            ast_left = True
    turning = ast_left
    turn += 1

ast = order[200 - 1]['coord']
print(f"Part two: {ast} gives {ast[0] * 100 + ast[1]}")
