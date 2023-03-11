import time
import typing
import asyncio
import threading

class FunctionCache(typing.TypedDict):
    result: typing.Any
    time: float

CallableType = typing.TypeVar("CallableType", typing.Callable, typing.Awaitable)

def cache(
        lifetime: int = float("inf"),
        suffix: str = "",
        save_memory: bool = False,
        values_filter: typing.Callable[..., bool] = lambda *args, **kwargs: True,
    ) -> typing.Callable:

    blacklist_values = blacklist_values or []
    storage: dict[str, FunctionCache] = {}
    
    def decorator(function: CallableType) -> CallableType:
        if asyncio.iscoroutinefunction(function):
            async def async_wrapper(*args, **kwargs) -> typing.Any:
                key = f"{suffix}{function.__name__}({args},{kwargs})"

                if key in storage and time.monotonic() - storage[key]["time"] < lifetime:
                    return storage[key]["result"]

                if values_filter(result := await function(*args, **kwargs)):
                    storage[key] = {"result": result, "time": time.monotonic()}

                return result
        
            return async_wrapper
        
        def sync_wrapper(*args, **kwargs) -> typing.Any:
            key = f"{suffix}{function.__name__}({args},{kwargs})"

            if key in storage and time.monotonic() - storage[key]["time"] < lifetime:
                return storage[key]["result"]
            
            if values_filter((result := function(*args, **kwargs))):
                storage[key] = {"result": result, "time": time.monotonic()}
            
            return result
        
        return sync_wrapper

    if save_memory:
        def clean_cache_daemon():
            while ...:
                current_time = time.monotonic()

                for key in list(storage.keys()):
                    if current_time - storage[key]["time"] >= lifetime:
                        del storage[key]

                time.sleep(lifetime // 2)

        threading.Thread(target=clean_cache_daemon, daemon=True).start()

    return decorator
