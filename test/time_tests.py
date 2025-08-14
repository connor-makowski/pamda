from pamda import pamda
from pamda.pamda_timer import pamda_timer

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

for function, args in [
    (pamda.groupBy, [lambda x: str(x["color"] + x["shape"]), data]),
    (pamda.groupKeys, [["color", "size"], data]),
    (pamda.nest, [["color", "size"], "size", data]),
    (pamda.nestItem, [["color", "size"], data]),
    (pamda.pluck, ["color", data]),
    (pamda.pluckIf, [lambda x: x["color"] == "red", ["color"], data]),
]:
    pamda_timer(function, iterations=3, print_time_stats=True).get_time_stats(*args)

