with open('input.txt', 'r') as file:
    input_masses = [int(x) for x in file.read().strip().split('\n')]


# One
def fuel(mass: int) -> int:
    return int(mass / 3) - 2


print(fuel(12), 'correct' if fuel(12) == 2 else 'error')
print(fuel(14), 'correct' if fuel(14) == 2 else 'error')
print(fuel(1969), 'correct' if fuel(1969) == 654 else 'error')
print(fuel(100756), 'correct' if fuel(100756) == 33583 else 'error')


total = sum([fuel(x) for x in input_masses])
print(f"Part one - total fuel: {total}")


# Two
def recursive_fuel(masses: []) -> []:
    fuels = []
    for mass in masses:
        fuel_part = fuel(mass)
        while fuel_part > 0:
            fuels.append(fuel_part)
            fuel_part = fuel(fuel_part)
    return fuels


print(recursive_fuel([1969]), 'correct' if sum(recursive_fuel([1969])) == 966 else 'error')
print(recursive_fuel([100756]), 'correct' if sum(recursive_fuel([100756])) == 50346 else 'error')


total_fuel = sum(recursive_fuel(input_masses))
print(f"Part two - total fuel: {total_fuel}")
