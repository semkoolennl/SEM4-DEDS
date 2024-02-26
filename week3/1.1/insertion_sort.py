from utils import *

def insertion_sort(arr: list[int]) -> None:
    for i in range(1, len(arr)):
        curr = arr[i]
        left = i - 1

        while left >= 0 and curr < arr[left]:
            arr[left + 1] = arr[left]
            left -= 1
        arr[left + 1] = curr

def execute():
    array = random_int_list(1_000)
    insertion_sort(array)

print_average_execution_time(execute) 
