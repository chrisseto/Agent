import asyncio
import functools

__version__ = '0.1.2'
__all__ = (
    'gen',
    'anext',
    'Result',
    'AsyncGenerator',
)


async def anext(gen):
    """The equivilent of next for async iterators

    Usage:
    >>> result = await anext(aiterable)
    """
    return await gen.__anext__()


def async_generator(func):
    """A decorator that turns the given function into an AsyncGenerator"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return AsyncGenerator(func(*args, **kwargs))
    return wrapper


class Result:
    """Wraps futures, or other values, so them may be properly yielded"""
    def __init__(self, inner):
        self.inner = inner


class AsyncGenerator:

    def __init__(self, gen):
        self.gen = gen

    async def __aiter__(self):
        """Makes this class an async *iteratable*

        Needs to return an async *iterator* which AsyncGenerator is
        See https://docs.python.org/3/glossary.html#term-asynchronous-iterable

        :returns: self
        """
        return self

    async def __anext__(self):
        """Makes this class an async *iterator*

        Spins the interal coroutine then either:
        Awaits futures returned and recalls itself
        Unwraps Result classes
        Otherwise returns the yielded value
        """
        try:
            item = next(self.gen)
        except StopIteration:
            raise StopAsyncIteration

        if isinstance(item, Result):
            return item.inner

        # Note: anything that is "yield from"ed or awaited
        # techincally just yields a Future
        # Impossible to actually tell if this was a yielded future or
        # A "yield from"ed future, hence Result
        if isinstance(item, asyncio.Future):
            await item
            return await self.__anext__()

        return item

# Nice aliases
gen = async_generator
