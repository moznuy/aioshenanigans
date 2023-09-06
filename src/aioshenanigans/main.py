from __future__ import annotations

import asyncio
import logging
import pprint
import signal
from collections.abc import Coroutine
from collections.abc import Iterable
from contextlib import AbstractAsyncContextManager
from typing import Any

logger = logging.getLogger(__name__)


CoroutineAnyReturn = Coroutine[None, None, Any]


def _signal_callback(quit_event: asyncio.Event) -> None:
    quit_event.set()


async def simple_main(coroutines: Iterable[CoroutineAnyReturn]) -> None:
    loop = asyncio.get_event_loop()

    quit_event = asyncio.Event()
    loop.add_signal_handler(signal.SIGINT, _signal_callback, quit_event)
    loop.add_signal_handler(signal.SIGTERM, _signal_callback, quit_event)

    tasks = [asyncio.create_task(coroutine) for coroutine in coroutines]

    await quit_event.wait()

    for task in tasks:
        task.cancel()
    res = await asyncio.gather(*tasks, return_exceptions=True)
    logger.debug("tasks : %s", pprint.pformat(res))


async def simple_main_factory(
    factory: Coroutine[None, None, Iterable[CoroutineAnyReturn]]
) -> None:
    coroutines = await factory
    await simple_main(coroutines)


async def simple_main_context(contex: AbstractAsyncContextManager[Any]) -> None:
    async with contex:
        await simple_main([])
