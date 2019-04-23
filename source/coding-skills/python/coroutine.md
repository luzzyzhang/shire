# Async IO & Coroutine

<!-- TOC -->

- [Async IO & Coroutine](#async-io--coroutine)
    - [Questions](#questions)
    - [Summary](#summary)
    - [Async IO](#async-io)
    - [Python `asyncio` package and `async/await`](#python-asyncio-package-and-asyncawait)
    - [Async IO design patterns](#async-io-design-patterns)
    - [When to use Async IO](#when-to-use-async-io)
    - [Example: Asynchrounous Requests](#example-asynchrounous-requests)
    - [Reference](#reference)

<!-- /TOC -->

## Questions

- What is Async IO
- How to use asyncio
- What is coroutine
- How to create native coroutine
- Relationship of coroutine and asyncio

## Summary

- Asynchronous IO as a language-agnostic model and a way to effect concurrency by letting **coroutines** indirectly communicate with each other
- The specifics of Python’s new `async` and `await` keywords, used to mark and define coroutines
- `asyncio`, the Python package that provides the API to run and manage coroutines

## Async IO

### What is Async IO

- Async IO is a style of concurrent programming, but it is not parallelism. It’s more closely aligned with threading than with multiprocessing but is very much distinct from both of these and is a standalone member in concurrency’s bag of tricks.
- Async IO is a single-threaded, single-process design: it uses cooperative multitasking.
- It has been said in other words that async IO gives a feeling of concurrency despite using a single thread in a single process.
- Coroutines (a central feature of async IO) can be scheduled concurrently, but they are not inherently concurrent.
- Asynchronous routines are able to “pause” while waiting on their ultimate result and let other routines run in the meantime.
- Asynchronous code, through the mechanism above, facilitates concurrent execution. To put it differently, asynchronous code gives the look and feel of concurrency.
- Async IO takes long waiting periods in which functions would otherwise be blocking and allows other functions to run during that downtime. (A function that blocks effectively forbids others from running from the time that it starts until the time that it returns.)
- Explain: 国际象棋大师1vn，饭店服务员点餐

### Where Async IO fit in

## Python `asyncio` package and `async/await`

### native coroutine

### rule of Async IO

## Async IO design patterns

## When to use Async IO

## Example: Asynchrounous Requests

```python
#!/usr/bin/env python3
# areq.py

"""Asynchronously get links embedded in multiple pages' HMTL."""

import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html

async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return found
    else:
        for link in HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        return found

async def write_one(file: IO, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info("Wrote results for source URL: %s", url)

async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent

    with open(here.joinpath("urls.txt")) as infile:
        urls = set(map(str.strip, infile))

    outpath = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tparsed_url\n")

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))
```

## Reference

- [real-python-async-io][1]

---
[1]: https://realpython.com/async-io-python