


import functools
import logging
import time


def retry(max_retries=3, delay=0.5, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error in {func.__name__}. Retry {retries + 1}/{max_retries}.")
                    retries += 1
                    if retries == max_retries:
                        raise e
                    time.sleep(delay * backoff ** retries)
        return wrapper
    return decorator