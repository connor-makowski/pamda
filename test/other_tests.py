from pamda import pamda
import time

print('\n===============\nOther Tests:\n===============')

# Type Enforcement
try:
    pamda.add('a',1)
    print('Type Enforcement Failed')
except:
    pass

# Async Testing
@pamda.thunkify
def test(name, wait):
    time.sleep(wait)
    return wait

async_test_a = pamda.asyncRun(test('a',2))
async_test_b = pamda.asyncRun(test('b',1))
async_test_a.asyncWait()
async_test_c = pamda.asyncRun(test('c',1))
