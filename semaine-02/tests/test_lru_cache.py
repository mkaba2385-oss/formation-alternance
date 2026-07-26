import time
import pytest
from lru_cache import LRUCache, lru_cache_decorator

#  Test 1 : opérations de base
def test_basic_get_put():
    cache = LRUCache(2)
    cache.put(1, 100)
    cache.put(2, 200)
    assert cache.get(1) == 100
    assert cache.get(2) == 200
    assert cache.get(3) is None

# Test 2 : politique d'éviction
def test_eviction_policy():
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    cache.get(1)
    cache.put(3, 30)
    assert cache.get(2) is None
    assert cache.get(1) == 10
    assert cache.get(3) == 30

# Test 3 : mise à jour
def test_update_existing_key():
    cache= LRUCache(2)
    cache.put(1,20)
    cache.put(2,30)
    cache.put(1,40)
    cache.put(3,30)
    assert cache.get(1) == 40
    assert cache.get(2) is None
    assert cache.get(3) == 30

# Test 4 : complexité O(1)

def test_time_complexity_is_o1():
    capacity = 100_000
    cache = LRUCache(capacity)
    for i in range(capacity):
        cache.put(i,i)
    
    start_time = time.perf_counter()
    for i in range(10_000):
        cache.get(i)
    elapsed_time = time.perf_counter() - start_time

    assert elapsed_time < 0.05

# Test 5 : décorateur Fibonacci

def test_fibonacci_decorator():
    @lru_cache_decorator(capacity=100)
    def fib(n: int):
        if n < 2:
            return n
        return fib(n-1)+fib(n-2)
    start_time = time.perf_counter()
    result = fib(35)
    elapsed_time = time.perf_counter() - start_time
    assert result == 9227465
    assert elapsed_time < 0.01


        