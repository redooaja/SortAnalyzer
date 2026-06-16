import time
import tracemalloc

def benchmark_algorithm(func, dataset, key):

    tracemalloc.start()

    start_time = time.perf_counter()

    sorted_data, comps, swaps = func(
        dataset,
        key
    )

    end_time = time.perf_counter()

    current_memory, peak_memory = (
        tracemalloc.get_traced_memory()
    )

    tracemalloc.stop()

    return {
        "sorted_data": sorted_data,
        "time": end_time - start_time,
        "comparisons": comps,
        "swaps": swaps,
        "peak_memory": peak_memory / 1024
    }