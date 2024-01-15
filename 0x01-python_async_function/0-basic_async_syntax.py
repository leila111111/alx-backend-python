#!/usr/bin/env python3
'''Task 0'''
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    ''' that waits for a random delay between 0 and max_delay'''

    delay = random.random() * max_delay
    await asyncio.sleep(delay)
    return delay
