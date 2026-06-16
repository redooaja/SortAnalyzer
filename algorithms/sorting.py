# =====================================================
# 1. IMPLEMENTASI ALGORITMA SORTING
# =====================================================

def bubble_sort(arr, key):
    arr = arr.copy()
    n = len(arr)

    comparisons = 0
    swaps = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1

            if arr[j][key] > arr[j + 1][key]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return arr, comparisons, swaps


def selection_sort(arr, key):
    arr = arr.copy()
    n = len(arr)

    comparisons = 0
    swaps = 0

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            comparisons += 1

            if arr[j][key] < arr[min_idx][key]:
                min_idx = j

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

    return arr, comparisons, swaps


def merge_sort(arr, key):
    comp = 0

    def merge(left, right):
        nonlocal comp

        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comp += 1

            if left[i][key] <= right[j][key]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    def sort(data):
        if len(data) <= 1:
            return data

        middle = len(data) // 2

        left = sort(data[:middle])
        right = sort(data[middle:])

        return merge(left, right)

    sorted_arr = sort(arr.copy())

    return sorted_arr, comp, 0


def quick_sort(arr, key):
    comp = 0

    def sort(data):
        nonlocal comp

        if len(data) <= 1:
            return data

        pivot = data[len(data) // 2]

        left = []
        middle = []
        right = []

        for item in data:
            comp += 1

            if item[key] < pivot[key]:
                left.append(item)

            elif item[key] == pivot[key]:
                middle.append(item)

            else:
                right.append(item)

        return sort(left) + middle + sort(right)

    sorted_arr = sort(arr.copy())

    return sorted_arr, comp, 0
