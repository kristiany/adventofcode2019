
with open('input.txt', 'r') as file:
    img = file.read().strip()

w = 25
h = 6


def get_layer(img, nr, w, h):
    return img[nr * w * h: (nr + 1) * w * h]


layers = int(len(img) / (w * h))
print(layers)

min_layer = None
min_zeros = w * h  # Start with max
for layer_nr in range(layers):
    layer = get_layer(img, layer_nr, w, h)
    zeros = layer.count('0')
    #print(f"Layer {layer_nr} got {zeros} zeros")
    if zeros < min_zeros:
        min_zeros = zeros
        min_layer = layer

ones = min_layer.count('1')
twos = min_layer.count('2')

print(f"Part one: {ones} * {twos} = {ones * twos}")


def decode(img, layers, w, h):
    final = []
    for p in range(w * h):
        for layer_nr in range(layers):
            layer = get_layer(img, layer_nr, w, h)
            nr = layer[p]
            if nr == '2':
                continue
            final.append(nr)
            break
    return final


test = '0222112222120000'
t_w = 2
t_h = 2
t_layers = int(len(test) / (t_w * t_h))
t_final = decode(test, t_layers, t_w, t_h)
print(f"Test final {t_final}")

final = decode(img, layers, w, h)
print(f"Part two: message 👇🏼")
for y in range(h):
    print(''.join([('  ' if p == '0' else u"\u2588" + u"\u2588") for p in final[y * w: y * w + w]]))
