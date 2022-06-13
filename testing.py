"""
Testing Timsort
---------------
Here we push timsort to the limits and test it
After testing, my implementation of timsort was the clear winner :)
"""
from merge_sort import merge_sort
from their_timsort import timsort as their_timsort
from count_runs import timsort as merges_natural_runs
from gallops import timsort as with_galloping
from timsort import timsort
from timeit import default_timer as timer
import random


def test(func, original_array, display, key=None, reverse=False, output_error=True):
    array = original_array.copy()
    sorted_array = sorted(array, key=key, reverse=reverse)
    kwargs = {}
    if key is not None: kwargs["key"] = key
    if reverse: kwargs["reverse"] = reverse
    try:
        start = timer()
        func(array, **kwargs)
        end = timer()
    except IndexError as e:
        if output_error:
            with open("error.log", mode="a") as f:
                f.write(f"{original_array}\n")
        raise IndexError(e)
    is_sorted = array == sorted_array
    print(f"({'XO'[is_sorted]}) {display:<35} {end-start}")
    if not is_sorted and output_error:
        with open("error.log", mode="a") as f:
            f.write(f"{original_array}\n")
    return array


# Test codes
n = 100000  # Length of array
rate_of_unsortedness = 1000  # The larger the value, the more sorted partially_sorted is
range_of_numbers = 10000
# Produce arrays for testing
partially_sorted = [i*(1,2)[not random.randint(0, rate_of_unsortedness)] for i in range(n)]
completely_random = [random.randint(0, range_of_numbers) for _ in range(n)]

# Functions to be tested
functions = {
    "merge sort": merge_sort,
    "their timsort": their_timsort,
    "merges natural runs": merges_natural_runs,
    "with galloping": with_galloping,
    "final timsort (with merge_at)": timsort
}.items()  # LOL

# Print Length of array
print("Sorting array of length", n)

# Test on completely random arrays
print("Completely Random:")
for display, sort_func in functions:
    test(sort_func, completely_random, display)

# Test on partially sorted arrays
print("Partially Sorted:")
for display, sort_func in functions:
    test(sort_func, partially_sorted, display)


# Test on reverse functionality
print("\nReversed:\n")

# Test on completely random arrays
print("Completely Random:")
for display, sort_func in functions:
    test(sort_func, completely_random, display, reverse=True)

# Test on partially sorted arrays
print("Partially Sorted:")
for display, sort_func in functions:
    test(sort_func, partially_sorted, display, reverse=True)
