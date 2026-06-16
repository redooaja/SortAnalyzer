# =====================================================
# 2. IMPLEMENTASI BINARY SEARCH
# =====================================================

def binary_search(arr, target_nim):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid]["NIM"] == target_nim:
            return arr[mid]

        elif arr[mid]["NIM"] < target_nim:
            low = mid + 1

        else:
            high = mid - 1

    return None