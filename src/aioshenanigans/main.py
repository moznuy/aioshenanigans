import asyncio
import logging
import pprint
import signal
from typing import Coroutine
from typing import Iterable

logger = logging.getLogger(__name__)


def _signal_callback(quit_event: asyncio.Event) -> None:
    quit_event.set()


async def simple_main(coroutines: Iterable[Coroutine]):
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


async def simple_main_factory(factory: Coroutine[None, None, Iterable[Coroutine]]):
    coroutines = await factory
    await simple_main(coroutines)
