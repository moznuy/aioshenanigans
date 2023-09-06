import asyncio
from collections.abc import Coroutine
from typing import Any

import pytest
import os
import signal
import contextlib
from typing import AsyncIterator

from aioshenanigans import simple_main
from aioshenanigans import simple_main_factory
from aioshenanigans import simple_main_context


async def big() -> None:
    while True:
        await asyncio.sleep(1)


async def small() -> None:
    await asyncio.sleep(1)


@pytest.mark.asyncio
async def test_simple_main() -> None:
    coroutines = [big(), small()]

    async def task() -> None:
        await asyncio.sleep(0.1)
        os.kill(os.getpid(), signal.SIGINT)

    t = asyncio.create_task(task())
    await simple_main(coroutines)
    t.cancel()
    await t


@pytest.mark.asyncio
async def test_simple_main_factory() -> None:
    async def helper() -> list[Coroutine[None, None, Any]]:
        return [big(), small()]

    async def task() -> None:
        await asyncio.sleep(0.1)
        os.kill(os.getpid(), signal.SIGINT)

    t = asyncio.create_task(task())
    await simple_main_factory(helper())
    t.cancel()
    await t


@pytest.mark.asyncio
async def test_simple_main_context() -> None:
    @contextlib.asynccontextmanager
    async def helper() -> AsyncIterator[None]:
        await small()
        yield
        await small()

    async def task() -> None:
        await asyncio.sleep(1.5)
        os.kill(os.getpid(), signal.SIGINT)

    t = asyncio.create_task(task())
    await simple_main_context(helper())
    t.cancel()
    await t
