import random

def random_int_list(length, min = 0, max = 1000):
    return [random.randint(min, max) for _ in range(length)]

def count_frequencies(int_list):
    frequency_dict = {}
    for number in int_list:
        if number in frequency_dict:
            frequency_dict[number] += 1
        else:
            frequency_dict[number] = 1
    return frequency_dict

def determine_highest_frequency(frequency_dict):
    highest_frequency = 0
    highest_number = 0
    for number, frequency in frequency_dict.items():
        if frequency > highest_frequency:
            highest_frequency = frequency
            highest_number = number
    return highest_number, highest_frequency


int_list = random_int_list(1000, 0, 100)
frequency_dict = count_frequencies(int_list)
highest_number, highest_frequency = determine_highest_frequency(frequency_dict)
print(f"The number {highest_number} occurs {highest_frequency} times in the list.")
