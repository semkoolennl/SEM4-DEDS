def reverse_string(input_str):
    # Convert the string to a list of characters
    char_list = list(input_str)
    
    # Use two pointers to reverse the string in-place
    left, right = 0, len(char_list) - 1
    while left < right:
        # Swap characters at the left and right pointers
        char_list[left], char_list[right] = char_list[right], char_list[left]
        
        # Move the pointers towards each other
        left += 1
        right -= 1
    
    # Convert the list of characters back to a string
    reversed_str = ''.join(char_list)
    
    return reversed_str

# Example usage:
input_str = "Hello, World!"
reversed_str = reverse_string(input_str)
print("Original String:", input_str)
print("Reversed String:", reversed_str)
