test = [111111, 555567, 155556, 223344, 345599, 223450, 123789, 555508, 555678, 666789, 123444]
input = range(264793, 803935 + 1)


def increasing(password):
    for i in range(1, 6):
        if int(password[i - 1]) > int(password[i]):
            return False
    return True


def two_adjacent(password):
    return len(set(list(password))) < 6


def only_two_adjacent(password):
    distribution = {}
    for c in password:
        if c in distribution:
            distribution[c] += 1
        else:
            distribution[c] = 1
    for d in distribution:
        if distribution[d] == 2:
            return True
    return False


def basic_validation(password):
    return len(password) == 6 and increasing(password)


def validate_one(password):
    return basic_validation(password) and two_adjacent(password)


def validate_two(password):
    return basic_validation(password) and only_two_adjacent(password)


def nr_of_valid(input, method):
    valid = 0
    for pin in input:
        if method(str(pin)):
            valid += 1
    return valid


print(f"Part one: number of valid passwords {nr_of_valid(input, validate_one)}")

print(f"Part two: number of valid passwords {nr_of_valid(input, validate_two)}")
