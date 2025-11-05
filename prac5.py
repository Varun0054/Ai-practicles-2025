"""Selection Sort (greedy) implementation and demo.

Selection sort is a classic example of a greedy algorithm: at each step it
selects the smallest remaining element and places it into its final position.
This module provides a simple implementation, a short explanation, and a demo
with assertions.
"""

from typing import List, Sequence


def selection_sort(data: Sequence[float], inplace: bool = False) -> List[float]:
	"""Sorts the given sequence using selection sort and returns the sorted list.

	Args:
		data: sequence of comparable items (numbers, strings, etc.).
		inplace: if True, sort a mutable copy in place and return it; if False,
				 work on a shallow copy and leave the original unchanged.

	Returns:
		A list with the elements of `data` sorted in non-decreasing order.

	Notes:
		- Selection sort repeatedly makes the greedy choice of selecting the
		  smallest remaining element and swapping it into position.
		- Time complexity: O(n^2) comparisons, O(n) swaps.
	"""
	arr = list(data) if not inplace else data  # if data is mutable and inplace True, we assume user knows
	# If user passed an immutable sequence and asked inplace=True, we already made a list copy
	if not isinstance(arr, list):
		arr = list(arr)

	n = len(arr)
	for i in range(n - 1):
		# Greedy choice: find index of minimum element in arr[i:]
		min_idx = i
		for j in range(i + 1, n):
			if arr[j] < arr[min_idx]:
				min_idx = j

		# Place minimum at position i (swap)
		if min_idx != i:
			arr[i], arr[min_idx] = arr[min_idx], arr[i]

	return arr


def _demo() -> None:
	print("Selection Sort (greedy) demo")

	example = [64, 25, 12, 22, 11]
	print("Before:", example)
	sorted_example = selection_sort(example)
	print("After:", sorted_example)

	# Basic correctness checks
	assert sorted_example == sorted(example), "selection_sort result differs from built-in sorted()"
	assert selection_sort([]) == [], "empty list should sort to empty list"
	assert selection_sort([1]) == [1], "single-element list should remain the same"
	assert selection_sort([2, 1]) == [1, 2], "two-element list must be sorted"

	# Demonstrate greedy property: at each step the earliest prefix is finalized
	arr = [3, 1, 4, 2]
	partial = list(arr)
	# run one iteration manually: select minimum from entire array and place at index 0
	min_idx = 0
	for j in range(1, len(partial)):
		if partial[j] < partial[min_idx]:
			min_idx = j
	partial[0], partial[min_idx] = partial[min_idx], partial[0]
	print("After one greedy choice step:", partial)

	print("All demo assertions passed.")


if __name__ == "__main__":
	_demo()

