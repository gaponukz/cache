import time
import typing
import asyncio
import threading

class FunctionCache(typing.TypedDict):
    result: typing.Any
    time: float

T = typing.TypeVar("T")
CallableType = typing.TypeVar("CallableType", typing.Callable, typing.Awaitable)

def cache(lifetime: int, blacklist_values: list = None, suffix: str = "", save_memory: bool = False) -> typing.Callable:
    blacklist_values = blacklist_values or []
    storage: dict[str, FunctionCache] = {}
    
    def decorator(function: CallableType) -> CallableType:
        if asyncio.iscoroutinefunction(function):
            async def async_wrapper(*args, **kwargs) -> typing.Any:
                key = f"{suffix}{function.__name__}_{args}_{kwargs}"

                if key in storage and time.monotonic() - storage[key]["time"] < lifetime:
                    return storage[key]["result"]

                if (result := await function(*args, **kwargs)) not in blacklist_values:
                    storage[key] = {"result": result, "time": time.monotonic()}

                return result
        
            return async_wrapper
        
        def sync_wrapper(*args, **kwargs) -> typing.Any:
            key = f"{suffix}{function.__name__}_{args}_{kwargs}"

            if key in storage and time.monotonic() - storage[key]["time"] < lifetime:
                return storage[key]["result"]
            
            if (result := function(*args, **kwargs)) not in blacklist_values:
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

        thread = threading.Thread(target=clean_cache_daemon)
        thread.daemon = True
        thread.start()

    return decorator
