import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, TypeVar
from functools import partial

T = TypeVar("T")
R = TypeVar("R")


async def run_sync_in_async(sync_func: Callable[[T], R], *args, **kwargs) -> R:
    """
    Runs a synchronous function in an async context without blocking.

    Args:
        sync_func: The synchronous function to run
        *args: Positional arguments to pass to the sync function
        **kwargs: Keyword arguments to pass to the sync function

    Returns:
        The result from the synchronous function
    """
    # Create a thread pool executor
    loop = asyncio.get_running_loop()

    # If we have arguments, create a partial function
    if args or kwargs:
        sync_func = partial(sync_func, *args, **kwargs)

    # Run the sync function in a thread pool
    return await loop.run_in_executor(None, sync_func)


def format_srt(srt: bytes) -> str:
    srt_txt = srt.decode("utf-8")
    blocks = srt_txt.split("\n\n")

    output = []
    for block in blocks:
        lines = block.split("\n")
        start_time, end_time = lines[1].split(" --> ")
        output.append(f"{start_time[:-4]}: {'\n'.join(lines[2:])}")
    return "\n\n".join(output)
