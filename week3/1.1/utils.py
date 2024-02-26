import random
import time

def random_int_list(length, min = 0, max = 1000):
    return [random.randint(min, max) for _ in range(length)]

def execute_and_time(func, *args):
    start = time.time()
    func(*args)
    end = time.time()
    return end - start

def average_execution_time(func, *args, n = 100):
    return sum(execute_and_time(func, *args) for _ in range(n)) / n

def print_average_execution_time(func, *args, n = 100):
    print(f"Average execution time: {average_execution_time(func, *args, n = n)*1000:.3f} ms")

def print_execution_time(func, *args):
    print(f"Execution time: {execute_and_time(func, *args)} seconds")
