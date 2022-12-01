from time import perf_counter
from multiprocessing import Pool
from threading import Thread
import asyncio

import requests
import aiohttp


def serial_visit(urls):
    return [requests.get(url).json() for url in urls]


def get_tasks(session, urls):
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(session.get(url, ssl=False)))
    return tasks


async def get_symbols():
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, urls)
        responses = await asyncio.gather(*tasks)
        return [(await response.json()) for response in responses]


if __name__ == "__main__":

    loop = 1
    urls = [
        "http://127.0.0.1:8000/genesets",
        "http://127.0.0.1:8000/genesets/1",
        "http://127.0.0.1:8000/genesets/search?title=",
        "http://127.0.0.1:8000/genes",
        "http://127.0.0.1:8000/genes/1",
        "http://127.0.0.1:8000/genes/search?name=",
    ]

    # sync:
    start = perf_counter()
    for i in range(loop):
        serial_visit(urls)
    end = perf_counter()
    print(f"Sync way took {round(end-start, 3)} seconds to make {loop*len(urls)} API calls")

    # multiprocessing
    start = perf_counter()
    p = Pool(4)
    for i in range(loop):
        p.apply_async(func=serial_visit, args=(urls,))
    p.close()
    p.join()
    end = perf_counter()
    print(f"Multiprocessing took {round(end-start, 3)} seconds to make {loop*len(urls)} API calls")

    # multithreading
    start = perf_counter()
    for i in range(loop):
        t = Thread(target=serial_visit, args=(urls,))
        t.start()
    t.join()
    end = perf_counter()
    print(f"Multithreading took {round(end-start, 3)} seconds to make {loop*len(urls)} API calls")

    # async:
    urls *= loop
    start = perf_counter()
    asyncio.run(get_symbols())
    end = perf_counter()
    print(f"Async way took {round(end-start, 3)} seconds to make {len(urls)} API calls")
