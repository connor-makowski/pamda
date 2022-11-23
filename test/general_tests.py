from pamda import pamda
import time

# Type Enforcement
try:
    pamda.add('a',1)
    print('Type Enforcement Failed')
except:
    pass

@pamda.thunkify
def test(name, wait):
    print(f'{name} start')
    time.sleep(wait)
    print(f'{name} end')
    return wait

async_test_a = pamda.asyncRun(test('a',2))
async_test_b = pamda.asyncRun(test('b',1))
async_test_a.asyncWait()
async_test_c = pamda.asyncRun(test('c',1))


def square(x):
    return x**2

def half(x):
    return x/2

def negate(x):
    return -x

data=6
# You can pipe data through multiple functions for clean functional programming
print(pamda.pipe([square, half, negate])(data)) #=> -18
