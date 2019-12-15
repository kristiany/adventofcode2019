import math

def load(file):
    with open(file, 'r') as file:
        return [parse(x) for x in file.read().strip().split('\n')]


class Reaction:
    def __init__(self, input_chems: (), output_chem: ()):
        self.inputs = input_chems
        self.output = output_chem

    def __str__(self):
        return f"{self.inputs} => {self.output}"


def parse(reaction_input):
    inputs = reaction_input.split('=>')[0].strip().split(',')
    input_chems = []
    for x in inputs:
        input_chems.append((x.strip().split(' ')[1], int(x.strip().split(' ')[0])))
    output = reaction_input.split('=>')[1]
    output_chem = (output.strip().split(' ')[1], int(output.strip().split(' ')[0]))
    return Reaction(input_chems, output_chem)


def find_reaction(reactions, chem_output):
    return [r for r in reactions if r.output[0] == chem_output][0]


def safe_add(inventory, key, value):
    if key not in inventory:
        inventory[key] = 0
    inventory[key] += value


def ores_rec(reactions, input, inventory):
    if input[0] == 'ORE':
        safe_add(inventory, 'ORE', input[1])
        #print(f"Consume {input[1]} ORE")
        return input[1]
    #print(f"Before: {inventory}")
    r = find_reaction(reactions, input[0])

    output = r.output[1]
    modified_input = input[1]
    if input[0] in inventory and inventory[input[0]] < 0:
        modified_input = max(r.output[1], -inventory[r.output[0]])

    multiplier = math.ceil(modified_input / output)
    safe_add(inventory, input[0], output * multiplier)  # Add reaction result to inventory
    #print(f"Produce {output * multiplier} {input[0]}")

    ores = 0
    # run and collect ore
    if multiplier > 0:
        for exec in r.inputs:  # * multiplier:
            if exec[0] not in inventory:
                inventory[exec[0]] = 0
            if exec[0] != 'ORE':
                inventory[exec[0]] -= exec[1] * multiplier
            #print(f"Consume {exec[1] * multiplier} {exec[0]}")
            if exec[0] == 'ORE' or inventory[exec[0]] < 0:  # On minus so we need to run the reaction to get more
                ores += ores_rec(reactions, (exec[0], exec[1] * multiplier), inventory)
    #print(f"After: {inventory}")
    return ores


def ores_for_fuel(reactions, fuels=1):
    inventory = {}
    ores = ores_rec(reactions, ('FUEL', fuels), inventory)
    #print(f"Ores: {ores}")
    return ores


assert ores_for_fuel(load('test1.txt')) == 31
assert ores_for_fuel(load('test2.txt')) == 165
assert ores_for_fuel(load('test3.txt')) == 13312
assert ores_for_fuel(load('test4.txt')) == 180697
assert ores_for_fuel(load('test5.txt')) == 2210736

reactions = load('input.txt')
result_per_fuel = ores_for_fuel(reactions)
print(f"Part one: {result_per_fuel} ores")

ores_in_stock = 1000000000000
print(f"Test 3: {ores_for_fuel(load('test3.txt'), 82892753)}")
print(f"Test 4: {ores_for_fuel(load('test4.txt'), 5586022)}")
print(f"Test 5: {ores_for_fuel(load('test5.txt'), 460664)}")



start = int(ores_in_stock / result_per_fuel)
end = ores_in_stock
closest = start
while True:

    test = start + int((end - start) / 2)
    print(f"Start {start}, end {end}, test {test}")
    result = ores_for_fuel(reactions, test)
    closest = test
    if result < ores_in_stock:
        start = test
    elif result > ores_in_stock:
        end = test
    else:
        break
    if end - start == 1:
        break

print(f"-1: fuel {closest - 1} costs {ores_for_fuel(reactions, closest - 1)} ores")
print(f" 0: fuel {closest} costs {ores_for_fuel(reactions, closest)} ores")
print(f"+1: fuel {closest + 1} costs {ores_for_fuel(reactions, closest + 1)} ores")
print(f"Part two: {closest} ores")
