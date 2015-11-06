# Agent: Async generators for humans

**agent** provides a simple decorator to create python 3.5 [asynchronous iterators](https://docs.python.org/3/reference/compound_stmts.html#async-for) via `yield`s

## Examples

Make people wait for things for no reason!
```python
import agent
import asyncio

@agent.gen  # Shorthand decorator
def wait_for_me():
  yield 'Like '
  yield from asyncio.sleep(1)
  yield 'the line '
  yield from asyncio.sleep(10)
  yield 'at '
  yield from asyncio.sleep(100)
  yield 'the DMV'

async for part in wait_for_me():
  print(part)
```

Paginate websites in an easy asynchronous manner.
```python
import agent
import aiohttp

@agent.async_generator
def gen():
  page, url = 0, 'http://example.com/paginated/endpoint'
  while True:
    resp = yield from aiohttp.request('GET', url, params={'page': page})
    resp_json = (yield from resp.json())['data']
    if not resp_json:
      break
    for blob in resp_json['data']:
      yield blob
    page += 1

# Later on....

async for blob in gen():
    # Do work
```


**The possibilities are endless!**

For additional, crazier, examples take a look in the [tests directory](tests/).


## Get it

```bash
$ pip install -U agent
```

## Caveats

`yield from` syntax must be used as `yield` in an `async def` block is a syntax error.

```python
async def generator():
  yield 1  # Syntax Error :(
```

`asyncio.Future`s can not be yielded directly, they must be wrapped by `agent.Result`.


## License

MIT licensed. See the bundled [LICENSE](LICENSE) file for more details.
