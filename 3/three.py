def waypoints(input):
    return [(x[:1], int(x[1:])) for x in input.split(',')]


with open('input.txt', 'r') as file:
    content = file.read().strip().split('\n')
    line1 = waypoints(content[0])
    line2 = waypoints(content[1])


def step(direction, x, y):
    if direction == 'U':
        y += 1
    elif direction == 'D':
        y -= 1
    elif direction == 'L':
        x -= 1
    elif direction == 'R':
        x += 1
    return x, y


def coords(line):
    result = set()
    x = 0
    y = 0
    step_count = 0
    for waypoint in line:
        direction = waypoint[0]
        steps = waypoint[1]
        for s in range(steps):
            x, y = step(direction, x, y)
            step_count += 1
            result.add((x, y, step_count))
    return result


coords1 = coords(line1)
coords2 = coords(line2)

intersections = set([x[:2] for x in coords1]).intersection(set([x[:2] for x in coords2]))
print(intersections)
min_dist = min([abs(x[0]) + abs(x[1]) for x in intersections])

print(f"Part one: min distance {min_dist}")


def find(pos, coords):
    for c in coords:
        if pos == c[:2]:
            return c
    raise Exception(f"Unknown pos {pos} in coordinate list {coords}")


step_counts = []
for i in intersections:
    steps1 = find(i, coords1)[2]
    steps2 = find(i, coords2)[2]
    step_counts.append(steps1 + steps2)

print(step_counts)
print(f"Part two: min steps {min(step_counts)}")


