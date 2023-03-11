import os
import time

import psutil
import unittest
from cache import cache

def get_memory_usege() -> int:
    return psutil.Process(os.getpid()).memory_info().rss

class TestCache(unittest.TestCase):
    def test_lifetime(self):
        @cache(lifetime=10)
        def add_one(number: int) -> int:
            time.sleep(2)
            return number + 1
        
        start = time.monotonic()
        add_one(1)
        self.assertTrue(time.monotonic() - start >= 2)

        start = time.monotonic()
        add_one(1)
        self.assertTrue(time.monotonic() - start < 0.001)

        time.sleep(10)

        start = time.monotonic()
        add_one(1)
        self.assertTrue(time.monotonic() - start >= 2)
    
    def test_values_filter(self):
        @cache(values_filter = lambda number: number < 5)
        def add_one(number: int) -> int:
            time.sleep(2)
            return number + 1
        
        start = time.monotonic()
        add_one(2)
        self.assertTrue(time.monotonic() - start >= 2)

        start = time.monotonic()
        add_one(2)
        self.assertTrue(time.monotonic() - start < 0.001)

        start = time.monotonic()
        add_one(3)
        self.assertTrue(time.monotonic() - start >= 2)

        start = time.monotonic()
        add_one(3)
        self.assertTrue(time.monotonic() - start < 0.001)

        start = time.monotonic()
        add_one(5)
        self.assertTrue(time.monotonic() - start >= 2)

        start = time.monotonic()
        add_one(5)
        self.assertTrue(time.monotonic() - start >= 2)
    
    def test_save_memory(self):
        @cache(save_memory = True, lifetime = 2)
        def add_one(number: int) -> int:
            return number + 1

        before = get_memory_usege()

        for i in range(10000000):
            add_one(i)
        
        self.assertTrue(get_memory_usege() > before)

        memory = get_memory_usege()

        time.sleep(4)

        self.assertTrue(get_memory_usege() < memory)

if __name__ == '__main__':
    unittest.main()
