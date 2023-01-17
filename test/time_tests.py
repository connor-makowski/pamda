from pamda import pamda
from pamda.pamda_timer import pamda_timer

print('\n===============\n1M Scale Time Tests:\n===============')

# Test Parameters
data_size = 1000000
sizes = 50000

# Caclulated data
n_per_group = int(data_size/4)
data = [
    {'color':'red', 'size':i%sizes, 'shape':'sphere'} for i in range(n_per_group)
]+[
    {'color':'blue', 'size':i%sizes, 'shape':'sphere'} for i in range(n_per_group)
]+[
    {'color':'red', 'size':i%sizes, 'shape':'cube'} for i in range(n_per_group)
]+[
    {'color':'blue', 'size':i%sizes, 'shape':'cube'} for i in range(n_per_group)
]

pamda_timer(pamda.groupBy)(lambda x: x['color']+x['shape'], data)
pamda_timer(pamda.groupKeys)(['color', 'size'], data)
pamda_timer(pamda.nest)(['color', 'size'], 'size', data)
pamda_timer(pamda.nestItem)(['color', 'size'], data)
