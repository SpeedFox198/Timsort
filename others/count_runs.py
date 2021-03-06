# This is my ver 1.0 of timsort.
# It merges natural runs.
# However, it does not perform galloping.


def timsort(array:list, key=None, reverse:bool=False) -> None:
    """ Sorts an array using timsort algorithm """

    n = len(array)  # Length of array
    remaining = n  # Length of array left that needs merging

    min_run = compute_minrun(n)  # Minimum length of a run

    # Stacks for storing runs and powers found
    runs = []
    powers = []

    low = 0  # Index of low limit of run
    while remaining:

        # Get length of next run
        count, decreasing = count_run(array, low, low+remaining-1, key=key, reverse=reverse)

        # If run is strictly descending, reverse run in-place
        if decreasing:
            reverse_run(array, low, low+count-1)

        # If length of run is less than minrun, extend run
        if count < min_run:
            force = min(min_run, remaining)  # Length to force size of run into
            bin_insertion_sort(array, low, low+force-1, key=key, reverse=reverse)
            count = force

        # Store value of current low and count
        curr_low, curr_count = low, count

        # If runs stack is not empty
        if runs:

            # Find power of run
            prev_low, prev_count = runs[-1]
            power = powerloop(prev_low, prev_count, curr_count, n)

            # While power is smaller than power at top of stack
            while powers and power <= powers[-1]:
                powers.pop()  # Remove old power from stack
                prev_prev_low, prev_prev_count = runs[-2]

                # Merge runs
                if prev_prev_count <= prev_count:
                    merge_lo(array, prev_prev_low, prev_prev_count, prev_low, prev_count, key=key, reverse=reverse)
                else:
                    merge_hi(array, prev_prev_low, prev_prev_count, prev_low, prev_count, key=key, reverse=reverse)

                runs.pop()  # Remove old prev run from stack
                runs[-1][1] += prev_count  # Set new low and count of current run
                prev_low, prev_count = runs[-1]  # Get updated values of previous run

            # Add power to stack
            powers.append(power)

        # Append to runs information of current run
        runs.append([curr_low, curr_count])

        remaining -= count  # Reduce remaining by length of run
        low += count

    curr_low, curr_count = runs[-1]
    for i in range(len(runs)-2, -1, -1):
        prev_low, prev_count = runs[i]
        
        # Merge runs
        if prev_count <= curr_count:
            merge_lo(array, prev_low, prev_count, curr_low, curr_count, key=key, reverse=reverse)
        else:
            merge_hi(array, prev_low, prev_count, curr_low, curr_count, key=key, reverse=reverse)

        # Calculate new low and count
        curr_low = prev_low
        curr_count += prev_count


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


def greater_than(x, y, key=None, reverse:bool=False) -> bool:
    """ Returns True if x is greater than y """

    # Call function if provided
    if key is not None:
        x = key(x)
        y = key(y)

    # Reverse process if reversed
    if reverse:
        return x < y
    else:
        return x > y


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


def powerloop(s1:int, n1:int, n2:int, n:int) -> int:
    """ Return power of run """
    power = 0  # power calculated

    # midpoints a and b:
    # a = s1 + n1/2
    # b = s1 + n1 + n2/2 = a + (n1 + n2)/2

    a = (2 * s1) + n1  # 2*a
    b = a + n1 + n2    # 2*b

    while True:
        power += 1

        if a >= n:  # n is before a
            a -= n
            b -= n

        elif b >= n:  # n is before b
            break

        # n is after a and b
        a <<= 1
        b <<= 1

    return power


def bin_insertion_sort(array:list, start:int, end:int, key=None, reverse:bool=False) -> None:
    """ Sorts an array using binary insertion sort algorithm """

    # Go through the elements and make comparisions
    for i in range(start+1, end+1):

        e = array[i]  # Current element

        j = i-1  # Index of element left of current element

        # Get index of position to insert element in
        pos = bin_search(array, e, start, j, key=key, reverse=reverse)

        # Shift elements to the right to perform insertion
        while j >= pos:
            array[j+1] = array[j]
            j -= 1

        # Insert element in sorted sub-array
        array[j+1] = e


def bin_search(array:list, target, low:int, high:int, key=None, reverse:bool=False) -> int:
    """ Binary searches the subarray for the index to insert element """

    # Loop till index out of range
    while low <= high:

        mid = (low + high) >> 1  # Index of middle element

        # If middle element is less than target
        if less_than(array[mid], target, key=key, reverse=reverse):
            low = mid + 1

        # If middle element is more than target
        elif greater_than(array[mid], target, key=key, reverse=reverse):
            high = mid - 1

        # If middle element matches target
        else:

            # Return index to insert element
            return mid + 1

    # Return low if not found
    return low


def count_run(array:list, low:int, high:int, key=None, reverse:bool=False) -> tuple[int, bool]:
    """ Returns the length of the run beginning at low """

    # If low is at end of list
    if low == high:
        return 1, False  # Return length of run, not decreasing

    count = 2  # Count of length of the run
    low += 1

    # If run is strictly decreasing
    if less_than(array[low], array[low-1], key=key, reverse=reverse):

        # Count length of natural run
        for i in range(low+1, high+1):

            # Break if is increasing
            if less_than(array[i], array[i-1], key=key, reverse=reverse):
                count += 1
            else:
                break
        
        # Return length of run, decreasing
        return count, True

    # Else, run is increasing
    else:

        # Count length of natural run
        for i in range(low+1, high+1):

            # Break if is decreasing
            if less_than(array[i], array[i-1], key=key, reverse=reverse):
                break
            else:
                count += 1
        
        # Return length of run, not decreasing
        return count, False


def reverse_run(array:list, low:int, high:int) -> None:
    """ Reverses a run from low to high in-place """
    while low < high:
        array[low], array[high] = array[high], array[low]
        low += 1
        high -= 1


def merge_lo(array:list, s1:int, n1:int, s2:int, n2:int, key=None, reverse:bool=False) -> int:
    """ Merges two runs A and B at index s1 and s2 with length n1 and n2 where n1 < n2 """

    # Copy elements of smaller run into temp array,
    # and leave the longer run at the right of original array
    # This decreases the amount of space needed to merge the 2 runs
    # merge_lo merges the runs when n1 < n2

    temp = array[s1:s1+n1]  # Create temp array storing smaller run A

    i = 0   # Pointer for A (in temp array)
    j = s2  # Pointer for B (in original array)
    k = s1  # Pointer for merging runs

    # Merge (copy) till either pointer i or j goes out of range
    while i < n1 and j < s2+n2:

        # If B[j] < A[i]
        if less_than(array[j], temp[i], key=key, reverse=reverse):
            array[k] = array[j]
            j += 1

        # Else A[i] <= B[j]
        else:
            array[k] = temp[i]
            i += 1

        k += 1

    # Copy temp content into array if any
    while i < n1:
        array[k] = temp[i]
        i += 1
        k += 1


def merge_hi(array:list, s1:int, n1:int, s2:int, n2:int, key=None, reverse:bool=False) -> int:
    """ Merges two runs A and B at index s1 and s2 with length n1 and n2 where n1 > n2 """

    # Copy elements of smaller run into temp array,
    # and leave the longer run at the left of original array
    # This decreases the amount of space needed to merge the 2 runs
    # merge_hi merges the runs when n1 > n2

    temp = array[s2:s2+n2]  # Create temp array storing smaller run B

    i = s1+n1-1  # Pointer for A (in original array)
    j = n2-1     # Pointer for B (in temp array)
    k = s2+n2-1  # Pointer for merging runs

    # Merge (copy) till either pointer i or j goes out of range
    while i >= s1 and j >= 0:

        # Else A[i] > B[j]
        if greater_than(array[i], temp[j], key=key, reverse=reverse):
            array[k] = array[i]
            i -= 1

        # Else B[j] >= A[i]
        else:
            array[k] = temp[j]
            j -= 1

        k -= 1

    # Copy temp content into array if any
    while j >= 0:
        array[k] = temp[j]
        j -= 1
        k -= 1
