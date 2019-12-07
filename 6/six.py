with open('input.txt', 'r') as file:
    orbs = file.read().strip().split('\n')


def parent_path(parents, start):
    it = parents[start]
    path = []
    while it != 'COM':
        path.append(it)
        it = parents[it]
    return path


parents = {'COM': None}
nodes = set()
for orb in orbs:
    l, r = orb.split(')')
    parents[r] = l
    nodes.add(l)
    nodes.add(r)


count = 0
for n in nodes:
    it = n
    while it != 'COM':
        count += 1
        it = parents[it]

print(f"Part one: {count}")


you_path = parent_path(parents, 'YOU')
san_path = parent_path(parents, 'SAN')
fast_path = set(you_path).symmetric_difference(set(san_path))
print(f"Part two: {len(fast_path)}")