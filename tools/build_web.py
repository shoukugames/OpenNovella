#!/usr/bin/env python3
"""Build the browser version (the story player with the demo story) into build/web/.

1. Draws the demo story's artwork and sounds (examples/demo/make_art.py).
2. Copies only what the player needs into build/web-src/: the opennovella package without the
   tkinter editor, the demo story and main.py.
3. Runs pygbag (https://pygame-web.github.io) on that folder.

Needs: pygame, pygbag (python3 -m pip install pygbag) and ffmpeg on PATH (or FFMPEG=/path),
which pygbag uses to convert sounds to OGG.
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "build", "web-src")
OUT = os.path.join(ROOT, "build", "web")


def main():
    subprocess.run([sys.executable, os.path.join(ROOT, "examples", "demo", "make_art.py")], check=True)
    shutil.rmtree(SRC, ignore_errors=True)
    skip = shutil.ignore_patterns("__pycache__", "*.pyc", "saves", "editor")
    shutil.copytree(os.path.join(ROOT, "opennovella"), os.path.join(SRC, "opennovella"), ignore=skip)
    shutil.copytree(os.path.join(ROOT, "examples", "demo"), os.path.join(SRC, "examples", "demo"),
                    ignore=shutil.ignore_patterns("make_art.py", "saves", "__pycache__"))
    shutil.copy(os.path.join(ROOT, "main.py"), SRC)
    ffmpeg = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    env = dict(os.environ)
    if ffmpeg:
        env["PATH"] = os.path.dirname(os.path.abspath(ffmpeg)) + os.pathsep + env.get("PATH", "")
    icon = os.path.join("opennovella", "icons", "opennovella-256.png")
    args = [sys.executable, "-m", "pygbag", "--build", "--title", "OpenNovella", "--app_name", "opennovella"]
    if os.path.exists(os.path.join(SRC, icon)):
        args += ["--icon", icon]
    subprocess.run(args + ["."], cwd=SRC, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.move(os.path.join(SRC, "build", "web"), OUT)
    if not os.path.exists(os.path.join(OUT, "index.html")):
        sys.exit("pygbag did not write index.html")
    print("build/web ready: upload the folder as-is")


if __name__ == "__main__":
    main()

# pygbag sometimes sizes the canvas before the game has opened its window, squeezing the game
# into a square: add a small script that keeps it the game's shape (tools/web_canvas_fix.py).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web_canvas_fix  # noqa: E402

web_canvas_fix.apply(os.path.join(ROOT, "build", "web", "index.html"))
