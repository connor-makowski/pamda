import pytest
import time
from pamda import pamda


def test_type_enforcement():
    with pytest.raises(Exception):
        pamda.add("a", 1)


def test_async_wait():
    @pamda.thunkify
    def sleeper(name, wait):
        waited = 0
        while waited < wait:
            time.sleep(0.1)
            waited += 0.1
        return wait

    start_time = time.time()
    async_test_a = sleeper("a", 0.3)
    async_test_b = sleeper("b", 0.2)
    async_test_a.asyncRun()
    async_test_b.asyncRun()
    async_test_a.asyncWait()
    async_test_b.asyncWait()
    async_time = time.time() - start_time
    assert 0.3 <= async_time < 1.5


def test_async_kill():
    @pamda.thunkify
    def sleeper(name, wait):
        waited = 0
        while waited < wait:
            time.sleep(0.1)
            waited += 0.1
        return wait

    start_time = time.time()
    async_test_a = sleeper("a", 0.3)
    async_test_b = sleeper("b", 0.2)
    async_test_a.asyncRun()
    async_test_b.asyncRun()
    time.sleep(0.1)
    async_test_a.asyncKill()
    async_test_b.asyncWait()
    async_time = time.time() - start_time
    assert 0.2 <= async_time < 1.5
