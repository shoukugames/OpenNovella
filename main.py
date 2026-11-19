"""Web entry point for pygbag (https://pygame-web.github.io): plays the demo story in the browser.

Build with:  python3 tools/build_web.py     (writes build/web/)
The editor needs a desktop (tkinter); on the desktop use start_editor.py or `python3 -m opennovella`.
"""
import asyncio
import sys
import os

import pygame  # noqa: F401  (must be imported here so pygbag loads pygame)

# Browser audio: the page mixes sound on its main thread, between the game's frames, so a small
# mixer buffer runs dry whenever a frame takes a little longer, and the sound crackles and drops
# out. 2048 samples (43 ms at the browser's 48 kHz) rides over slow frames. Browser only.
if sys.platform == "emscripten":
    WEB_AUDIO_BUFFER = 2048

    def _web_audio_buffer(fn):
        def call(*args, **kwargs):
            if len(args) >= 4:
                args = args[:3] + (WEB_AUDIO_BUFFER,) + args[4:]
            else:
                kwargs["buffer"] = WEB_AUDIO_BUFFER
            return fn(*args, **kwargs)
        return call

    pygame.mixer.pre_init = _web_audio_buffer(pygame.mixer.pre_init)
    pygame.mixer.init = _web_audio_buffer(pygame.mixer.init)
    pygame.mixer.pre_init()

from opennovella.player import Player
from opennovella.story import load_story

HERE = os.path.dirname(os.path.abspath(__file__))


async def main():
    await Player(load_story(os.path.join(HERE, "examples", "demo"))).run_web()


asyncio.run(main())
