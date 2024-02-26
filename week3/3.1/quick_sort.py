from utils import print_average_execution_time, random_int_list

def partition(array, low, high):
     # Get the rightmost element of array as pivot
    pivot = array[high]
    
    # Pointer to the greater element
    pointer = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            # If element smaller than pivot, swap it with greater element 
            pointer = pointer + 1

            # Swapping element at pointer with element at j
            (array[pointer], array[j]) = (array[j], array[pointer])

    # Swap the pivot element with the greater element specified by pointer
    (array[pointer + 1], array[high]) = (array[high], array[pointer + 1])

    return pointer + 1
     

def quicksort_rec(array, low, high):
    if low < high:
        # Find the pivot index
        pivot = partition(array, low, high)

        quicksort_rec(array, low, pivot - 1)
        quicksort_rec(array, pivot + 1, high)


def quicksort(array):
    quicksort_rec(array, 0, len(array) - 1)

def exec():
    array = random_int_list(1_000)
    quicksort(array)

print_average_execution_time(exec)

