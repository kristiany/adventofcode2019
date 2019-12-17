def load(file):
    with open(file, 'r') as file:
        return [int(x) for x in list(file.read().strip())]


def fft(data, phases=100):
    for _ in range(phases):
        step = 1
        for i in range(0, len(data)):
            total = 0
            add = False
            factor = 1
            for s in range(0, len(data)):
                if (s + 1) % step == 0:
                    if add:
                        factor *= -1
                    add = not add
                if add:
                    total += data[s] * factor
            data[i] = abs(total) % 10
            step += 1
    return ''.join([str(c) for c in data[:8]])


# As I got stuck on part two, this one is highly inspired by:
#     https://www.reddit.com/r/adventofcode/comments/ebai4g/2019_day_16_solutions/fb58mb8/
def fft2(data):
    tail = int(''.join([str(n) for n in data[:7]]))
    data = (10000 * data)[tail:]
    for _ in range(100):
        for i in range(len(data) - 1, 0, -1):  # Backwards is key ¯\_(ツ)_/¯
            data[i - 1] = (data[i - 1] + data[i]) % 10  
    return ''.join([str(c) for c in data[:8]])


test1 = [int(x) for x in list("12345678")]
assert fft(test1, 4) == '01029498'

test2 = [int(x) for x in list("80871224585914546619083218645595")]
assert fft(test2)[:8] == '24176176'
test3 = [int(x) for x in list("19617804207202209144916044189917")]
assert fft(test3)[:8] == '73745418'
test4 = [int(x) for x in list("69317163492948606335995924319873")]
assert fft(test4)[:8] == '52432133'

input = load('input.txt')
print(f"Part one: {fft(input)}")

test5 = [int(x) for x in list("03036732577212944063491565474664")]
assert fft2(test5) == '84462026'
test6 = [int(x) for x in list("02935109699940807407585447034323")]
assert fft2(test6) == '78725270'
test7 = [int(x) for x in list("03081770884921959731165446850517")]
assert fft2(test7) == '53553731'

input = load('input.txt')
print(f"Part two: {fft2(input)}")
