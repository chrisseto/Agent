import agent
import pytest
import asyncio


@pytest.mark.asyncio
async def test_generator():

    @agent.async_generator
    def inner_gen():
        yield 0
        yield 1
        yield from asyncio.sleep(.01)
        yield 2
        yield from asyncio.sleep(.01)
        yield 3

    gen = inner_gen()
    assert isinstance(gen, agent.AsyncGenerator)
    assert hasattr(gen, '__anext__')
    assert hasattr(gen, '__aiter__')

    returns = iter(range(4))
    async for i in inner_gen():
        assert i == next(returns)


@pytest.mark.asyncio
async def test_anext():
    fut = asyncio.coroutine(lambda: (0, 1, 2, 3, 4, 5, 6))()

    @agent.async_generator
    def inner_gen():
        for x in (yield from fut):
            yield x

    gen = inner_gen()
    for i in range(6):
        assert i == await agent.anext(gen)


@pytest.mark.asyncio
async def test_coroutines():

    @agent.async_generator
    def inner_gen():
        yield from asyncio.coroutine(lambda: 'Not sent')()
        yield (yield from asyncio.coroutine(lambda: 'yield_from')())
        yield asyncio.coroutine(lambda: 'yield')()

    gen = inner_gen()
    assert await agent.anext(gen) == 'yield_from'
    assert await (await agent.anext(gen)) == 'yield'


@pytest.mark.asyncio
async def test_futures():

    @agent.async_generator
    def inner_gen():
        fut = asyncio.Future()
        fut.set_result(10)
        yield agent.Result(fut)

    gen = inner_gen()
    assert await (await agent.anext(gen)) == 10
