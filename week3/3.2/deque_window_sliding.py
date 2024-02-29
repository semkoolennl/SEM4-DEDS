from collections import deque

def sliding_window_max(nums, k):
    result = []  # Lijst om het maximale element in elk venster op te slaan
    dq = deque()  # Deque om de indexen van de elementen in het huidige venster op te slaan

    for i, num in enumerate(nums):
        # Verwijder elementen die buiten het huidige venster vallen
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Verwijder alle elementen die kleiner zijn dan het huidige element
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Voeg het maximale element in het huidige venster toe aan het resultaat
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# Voorbeeldgebruik
nums = [4, 2, 1, 7, 8, 1, 2, 8, 10]
k = 3
result = sliding_window_max(nums, k)

# [4, 7, 8, 8, 8, 8, 10]
print(result)
