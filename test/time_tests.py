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

# groupBy
@pamda_timer
def test_groupBy():
    pamda.groupBy(lambda x: x['color']+x['shape'], data)

# groupKeys
@pamda_timer
def test_groupKeys():
    pamda.groupKeys(['color', 'size'], data)

# nest
@pamda_timer
def test_nest():
    pamda.nest(['color', 'size'], 'size', data)

# nestItem
@pamda_timer
def test_nestItem():
    pamda.nestItem(['color', 'size'], data)

test_groupBy()
test_groupKeys()
test_nest()
test_nestItem()