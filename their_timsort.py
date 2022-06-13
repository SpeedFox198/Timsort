# This timsort was implemented using the same algorithm as
# the most common online implementations of timsort
# e.g. https://www.geeksforgeeks.org/timsort/
# It does not contain the real features of the
# actual imsort algorithm


def timsort(array:list, key=None, reverse:bool=False) -> None:
    """ Sorts an array using timsort algorithm """

    n = len(array)  # Length of array
    size = compute_minrun(n)  # Size of runs to merge

    # Sort runs using insertion sort
    for start in range(0, n, size):
        end = min(n, start+size) - 1
        insertion_sort(array, start, end, key=key, reverse=reverse)

    # Merge runs
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


def compute_minrun(n:int) -> int:
    """ Computes and return the minimum length of a run from 16 - 32 """

    # As python implemetation of insertion sort is not fast enough
    # minrun is from range 16 to 32 instead of range 32 to 64

    r = 0  # Becomes 1 if any 1 bits are shifted off

    # Take the first 5 bits of n
    while n >= 32:
        r |= n & 1
        n >>= 1

    # Return calculated value of min run
    return n + r


def insertion_sort(array:list, start:int, end:int, key=None, reverse:bool=False) -> None:
    """ Sorts an array using binary insertion sort algorithm """

    # Go through the elements and make comparisions
    for i in range(start+1, end+1):

        e = array[i]  # Current element

        j = i-1  # Index of element left of current element

        # Shift all elements greater than e to the right
        while j >= start and less_than(e, array[j], key=key, reverse=reverse):
            array[j+1] = array[j]
            j -= 1

        # Insert element in sorted sub-array
        array[j+1] = e


def merge(array:list, left:int, mid:int, right:int, key=None, reverse:bool=False) -> None:
    """ Merges the two sorted runs """

    # Temporary arrays
    run_a = array[left:mid]
    run_b = array[mid:right]

    # Size of arrays
    na = mid - left   # Length of run A
    nb = right - mid  # Length of run B

    # Pointers
    i, j, k = 0, 0, left

    # Merge the two runs
    while i < na and j < nb:
        if less_than(run_b[j], run_a[i], key=key, reverse=reverse):
            array[k] = run_b[j]
            j += 1

        else:
            array[k] = run_a[i]
            i += 1

        k += 1

    # Copy remaining elements of run A
    while i < na:
        array[k] = run_a[i]
        i += 1
        k += 1

    # Copy remaining element of run B
    while j < nb:
        array[k] = run_b[j]
        j += 1
        k += 1
