from pamda import pamda
from pamda.pamda_timer import pamda_timer
from pamda.pamda_fast import __assocPath__
import random


# seed the random number generator for reproducibility
random.seed(42)

print("\n===============\n1M Scale Time Tests:\n===============")

# Test Parameters
data_size = 1000000
sizes = 50000

# Caclulated data
n_per_group = int(data_size / 4)
data = (
    [
        {"color": "red", "size": i % sizes, "shape": "sphere"}
        for i in range(n_per_group)
    ]
    + [
        {"color": "blue", "size": i % sizes, "shape": "sphere"}
        for i in range(n_per_group)
    ]
    + [
        {"color": "red", "size": i % sizes, "shape": "cube"}
        for i in range(n_per_group)
    ]
    + [
        {"color": "blue", "size": i % sizes, "shape": "cube"}
        for i in range(n_per_group)
    ]
)

# Make a simple 10 tier nested structure for testing mergeDeep with random keys in each layer
data_merge_a = {}
for i in range(int(data_size/2)):
    path = [f'level{random.randint(1, 10)}' for _ in range(10)]
    __assocPath__(path, random.randint(1, 10), data_merge_a)

data_merge_b = {}
for i in range(int(data_size/2)):
    path = [f'level{random.randint(1, 10)}' for _ in range(10)]
    __assocPath__(path, random.randint(1, 10), data_merge_b)

data_zip_a = list(range(int(data_size/2)))
data_zip_b = list(range(int(data_size/2), data_size))

unflat_data = [[i] for i in range(data_size)]

for function, args in [
    (pamda.flatten, [unflat_data]),
    (pamda.groupBy, [lambda x: str(x["color"] + x["shape"]), data]),
    (pamda.groupKeys, [["color", "size"], data]),
    (pamda.groupWith, [lambda x,y: x["color"]==y["color"], data]),
    (pamda.mergeDeep, [data_merge_a, data_merge_b]),
    (pamda.nest, [["color", "size"], "size", data]),
    (pamda.nestItem, [["color", "size"], data]),
    (pamda.pivot, [data]),
    (pamda.pluck, ["color", data]),
    (pamda.pluckIf, [lambda x: x["color"] == "red", ["color"], data]),
    (pamda.project, [['color', 'size'], data]),
    (pamda.unnest, [unflat_data]),
    (pamda.zip, [data_zip_a, data_zip_b]),
    (pamda.zipObj, [data_zip_a, data_zip_b]),
]:
    pamda_timer(function, iterations=3, print_time_stats=True).get_time_stats(*args)

