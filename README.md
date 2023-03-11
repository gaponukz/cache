# cache decorator

```python
@cache(lifetime=10)
def long_function(*args, **kwargs):
  ...

long_function() # few seconds
long_function() # in one moment

# after 10 seconds

long_function() # again few seconds
```

## parameters
| Parameter | Type | Description |
| :--- | :--- | :--- |
| lifetime | `int` | The number of seconds that a cache entry should live before expiring. |
| values_filter | `callable -> bool` | Filter for values that should be cached. |
| suffix | `str` | A string that is added to the cache key to differentiate it from other cache entries. This is useful when multiple instances of the same function need to be cached. |
| save_memory | `bool` | A boolean flag that indicates whether a background thread should be started to periodically clean up expired cache entries and free up memory. |

## What's under the hood
This code implements a caching decorator that can be used to cache the results of a function with the ability to set a time-to-live for each cache entry. The decorator uses a dictionary to store the cache entries, and each entry consists of the result of the function and the time when it was added to the cache.

The decorator has two modes: synchronous and asynchronous. If the decorated function is a coroutine function, the decorator uses an asynchronous wrapper to execute the function and cache its result. Otherwise, the decorator uses a synchronous wrapper.
