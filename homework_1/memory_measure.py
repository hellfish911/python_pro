"""Module for measuring memory usage of functions using a decorator.

This module provides a decorator that utilizes the `tracemalloc` module to
track memory allocations during the execution of a function. After the
function finishes, the decorator prints both the current and peak memory
usage in megabytes (MB).
"""

import functools
import tracemalloc


def measure_memory(func):
    """Measure the memory usage of the decorated function.

    This decorator starts memory tracking before the function call and stops it
    afterward. It then retrieves and prints the current and peak memory usage
    during the function execution.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with memory usage measurement.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Measure memory usage during execution.

        Args:
            *args: Positional arguments passed to the decorated function.
            **kwargs: Keyword arguments passed to the decorated function.

        Returns:
            Any: The result of the decorated function.
        """
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(
            f'Memory usage for {func.__name__}: '
            f'Current = {current / 10**6:.6f} MB, '
            f'Peak = {peak / 10**6:.6f} MB'
        )
        return result

    return wrapper


@measure_memory
def generate_list(n: int) -> list:
    """Generate a list of integers from 0 to n-1.

    Args:
        n (int): The number of elements in the list.

    Returns:
        list: A list containing integers from 0 to n-1.
    """
    return [i for i in range(n)]


if __name__ == '__main__':
    generate_list(1_000_000)
