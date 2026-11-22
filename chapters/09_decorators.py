# Chapter 9: decorators.
import functools
import time


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f} s")
        return result
    return wrapper


@timed  # same as: count_words = timed(count_words)
def count_words(text):
    """How many words a text has."""
    return len(text.split())


print(count_words("the quick brown fox " * 10_000))
print(count_words.__name__, "-", count_words.__doc__)
