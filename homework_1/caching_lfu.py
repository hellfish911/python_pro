"""
Module implementing an LFU (Least Frequently Used) caching decorator.

This module provides a decorator that caches function results based on the LFU
strategy. When the cache size exceeds a specified maximum limit, the entry with
the lowest usage frequency is evicted.

It also includes an example function, `fetch_url`, which retrieves content from
URL using the `requests` library and returns the first N bytes of the content.
"""

import functools
import requests
from typing import Callable


def lfu_cache(max_limit: int = 64) -> Callable:
    """LFU cache decorator.

    This decorator caches the results of the decorated function using Least
    Frequently Used (LFU) strategy. When the cache reaches the `max_limit`, it
    evicts the entry with the lowest usage frequency.

    Args:
        max_limit (int, optional): Maximum number of entries allowed in cache.
            Defaults to 64.

    Returns:
        Callable: A decorator that wraps the target function with LFU caching.
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        usage = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Implement LFU caching for the decorated function.

            Args:
                *args: Positional arguments for the function.
                **kwargs: Keyword arguments for the function.

            Returns:
                Any: The result of the function, either from cache or computed.
            """
            # Create a key based on the function's arguments.
            # For kwargs, use a sorted tuple for consistency.
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                usage[key] += 1
                return cache[key]
            result = func(*args, **kwargs)
            if len(cache) >= max_limit:
                # Find the key with the minimum usage frequency and remove it.
                least_used_key = min(usage, key=usage.get)
                cache.pop(least_used_key)
                usage.pop(least_used_key)
            cache[key] = result
            usage[key] = 1
            return result

        # Expose the cache and usage dictionaries for external access.
        wrapper.cache = cache
        wrapper.usage = usage
        return wrapper
    return decorator


@lfu_cache(max_limit=64)
def fetch_url(url: str, first_n: int = 100) -> bytes:
    """Fetch a given URL and return the first_n bytes of its content.

    This function sends an HTTP GET request to the specified URL using the
    `requests` library. It returns the first `first_n` bytes of the response
    content. If `first_n` is set to zero, the entire content is returned.

    Args:
        url (str): The URL to be fetched.
        first_n (int, optional): The number of bytes to return from the fetched
            content. Defaults to 100.

    Returns:
        bytes: The content retrieved from the URL, truncated to the first
            `first_n` bytes if `first_n` is not zero.
    """
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


def main():
    """Use LFU cache module."""
    test_url = 'https://www.google.com'
    # Fetch the first 150 bytes.
    content = fetch_url(test_url, first_n=150)
    print('Fetched content (first 150 bytes):')
    print(content)

    # Call again to demonstrate cache hit.
    cached_content = fetch_url(test_url, first_n=150)
    print('Cached content (first 150 bytes):')
    print(cached_content)

    # Display cache keys and usage statistics.
    print('Cache keys:', fetch_url.cache)
    print('Usage counts:', fetch_url.usage)


if __name__ == '__main__':
    main()
