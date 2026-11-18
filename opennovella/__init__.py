"""OpenNovella - an easy-to-use visual novel engine written in Python.

Created by Shawn Rapaz and Claude Code.
"""

__version__ = "0.1.1"
__authors__ = ["Shawn Rapaz", "Claude Code"]
__credits__ = "OpenNovella was created by Shawn Rapaz and Claude Code."
__license__ = "GPL-3.0-or-later"

# True when running in a web browser (pygbag / WebAssembly).
import sys as _sys  # noqa: E402
WEB = _sys.platform == "emscripten"

import os as _os  # noqa: E402

# PNG copies of the app logo (packaging/debian/opennovella.svg) for window icons
ICON_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "icons")
ICON_SIZES = (16, 32, 48, 64, 128, 256)

from .story import Story, load_story, create_project  # noqa: E402

__all__ = ["Story", "load_story", "create_project", "__version__"]
