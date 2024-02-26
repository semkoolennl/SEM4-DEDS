import time
from utils import random_int_list

def partition(array, low, high):
    pass

def quicksort(array, low, high):
    if low < high:
        # Find the pivot index
        pivot = partition(array, low, high)

        quicksort(array, low, pivot - 1)
        quicksort(array, pivot + 1, high)
