"""Web entry point for pygbag (https://pygame-web.github.io): plays the demo story in the browser.

Build with:  python3 tools/build_web.py     (writes build/web/)
The editor needs a desktop (tkinter); on the desktop use start_editor.py or `python3 -m opennovella`.
"""
import asyncio
import os

import pygame  # noqa: F401  (must be imported here so pygbag loads pygame)

from opennovella.player import Player
from opennovella.story import load_story

HERE = os.path.dirname(os.path.abspath(__file__))


async def main():
    await Player(load_story(os.path.join(HERE, "examples", "demo"))).run_web()


asyncio.run(main())
