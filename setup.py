import cx_Freeze
from settings import *
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


includes = ["main.py", "sssnake.py", "README.md", "score", SNAKE_HEAD, APPLE, BITE, PUNCH, FONT_NAME, ICON]
includes.extend(SONGS)

cx_Freeze.setup(
    name="sssnake",
    author="Pekka Alho",
    options={"build_exe": {"packages": ["pygame"], "include_files": includes}},
    description="...",
    executables=[cx_Freeze.Executable("main.py")]
    )