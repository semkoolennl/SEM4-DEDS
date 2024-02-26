from utils import random_int_list, print_average_execution_time

def bubble_sort(arr):
	arr_length = len(arr)

    # Voorkom onnodig sorting
	is_swapped = False
	
	# Iterate over alle elements
	for i in range(arr_length-1):
		for j in range(0, arr_length-i-1):
			if arr[j] > arr[j + 1]:
				is_swapped = True
				arr[j], arr[j + 1] = arr[j + 1], arr[j]

		# Mocht er nergens een swap gedaan zijn, is hij al gesorteerd.
		if not is_swapped:
			return


def test():
    # Test performance
    bubble_sort(random_int_list(1000))

print_average_execution_time(test)
