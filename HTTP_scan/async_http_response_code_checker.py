#!/usr/bin/env python3
"""
Read a lists of IP addresses from file and performs a HEAD request.
Outputs HTTP response code, IP address and HTTP headers.
"""

import asyncio
import time
import aiohttp
from pathlib import Path
import sys


async def get_header(session, ip):
    async with session.head(f"http://{ip}/", allow_redirects=False) as response:
        print(response.status, ip, response.raw_headers)

async def get_headers(ip_addresses):
    headers = {"Connection":"close", "User-Agent":"Applicatie scopuri educationale. Contact: sea@gmx.es"}
    timeout = aiohttp.ClientTimeout(sock_connect=5, sock_read=5)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        tasks = []
        for ip in ip_addresses:
            task = asyncio.ensure_future(get_header(session, ip.strip()))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__== "__main__":
    filepath = Path(sys.argv[1])
    with filepath.open("r", encoding="utf-8") as file:
        ip_addresses = file.readlines()

    start_time = time.time()
    asyncio.run(get_headers(ip_addresses))
    print(f"Executed in: {time.time() - start_time}.")
