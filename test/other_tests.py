from pamda import pamda
import time

print("\n===============\nOther Tests:\n===============")

# Type Enforcement
try:
    pamda.add("a", 1)
    print("Type Enforcement Failed")
except:
    pass


# Async Testing
@pamda.thunkify
def sleeper(name, wait):
    waited = 0
    while waited < wait:
        # Note: Async kill does not kill sleeping threads
        # Once the sleep finishes, the thread is killed
        time.sleep(1)
        waited += 1
        # print(f'{name} has waited {waited} seconds')
    return wait


try:
    start_time = time.time()
    async_test_a = sleeper("a", 3)
    async_test_b = sleeper("b", 2)
    async_test_a.asyncRun()
    async_test_b.asyncRun()
    async_test_a.asyncWait()
    async_test_b.asyncWait()
    async_time = time.time() - start_time
    if async_time < 3 or async_time > 3.05:
        print("anyncWait Test Failed")
except:
    print("asyncWait Test Failed")

try:
    start_time = time.time()
    async_test_a = sleeper("a", 3)
    async_test_b = sleeper("b", 2)
    async_test_a.asyncRun()
    async_test_b.asyncRun()
    time.sleep(1)
    async_test_a.asyncKill()
    async_test_b.asyncWait()
    async_time = time.time() - start_time
    if async_time < 2 or async_time > 2.05:
        print("asyncKill Test Failed")
except:
    print("asyncKill Test Failed")
