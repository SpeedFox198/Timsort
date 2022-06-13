# The below is an implementation of merge sort

def merge_sort(array:list, key=None, reverse:bool=False) -> None:
    """ Sorts an array using the merge sort algorithm """

    n = len(array)  # Length of array
    size = 1  # Size of subarrays to merge

    # Merge subarrays
    while size < n:
        # Go through each run of size `size`
        for left in range(0, n, size << 1):

            # Get mid and right limits indexes of the runs
            # mid is the start index of 2nd run
            # right is the last index of 2nd run + 1
            mid = min(n, left + size)
            right = min(n, left + 2*size)

            # Merge runs if length of run is not 0
            if mid <= right:
                merge(array, left, mid, right, key=key, reverse=reverse)

        # Increase size
        size <<= 1


def merge(array:list, left:int, mid:int, right:int, key=None, reverse:bool=False) -> None:
    """ Merges the two sorted subarrays """

    # Temporary arrays
    array_a = array[left:mid]
    array_b = array[mid:right]

    # Size of arrays
    na = mid - left   # Length of subarray A
    nb = right - mid  # Length of subarray B

    # Pointers
    i, j, k = 0, 0, left

    # Merge the two subarrays
    while i < na and j < nb:
        if less_than(array_b[j], array_a[i], key=key, reverse=reverse):
            array[k] = array_b[j]
            j += 1

        else:
            array[k] = array_a[i]
            i += 1

        k += 1

    # Copy remaining elements of subarray A
    while i < na:
        array[k] = array_a[i]
        i += 1
        k += 1

    # Copy remaining element of subarray B
    while j < nb:
        array[k] = array_b[j]
        j += 1
        k += 1


def less_than(x, y, key=None, reverse:bool=False) -> bool:
    """ Returns True if x is less than y """

    # Call function if provided
    if key is not None:
        x = key(x)
        y = key(y)

    # Reverse process if reversed
    if reverse:
        return x > y
    else:
        return x < y
