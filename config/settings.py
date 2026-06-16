from algorithms.sorting import (
    bubble_sort,
    selection_sort,
    merge_sort,
    quick_sort
)

algorithms = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

complexities = {
    "Bubble Sort": "O(n²)",
    "Selection Sort": "O(n²)",
    "Merge Sort": "O(n log n)",
    "Quick Sort": "O(n log n)"
}