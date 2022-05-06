import sys
import glob
import os
from cx_Freeze import Executable, setup

files = glob.glob(os.path.join("src", "*.ini"), recursive=True) + glob.glob(os.path.join("src", "*.log"),
                                                                            recursive=True)
for file in files:
    os.remove(file)

version = "0.0"
base = 'Win32GUI' if sys.platform == 'win32' else None
targetName = "App.exe" if sys.platform == 'win32' else "App"

target = Executable(
    script="./src/main.py",
    base=base,
    target_name=targetName,
    manifest="MANIFEST.in",
    icon="./src/assets/icons/logo.ico"
)

options = {
    'build_exe': ".\\build\\windows\\{0}\\exe\\_Files".format(version),
    'excludes': ["tkinter", "PyQt6", "PyQt5.Qt5.qml", "lib.test", 
                 "src.assets.resources", "src.assets.startup.server"]
}

setup(
    name="App",
    version=version,
    description="Engineering Application",
    author="David Rees",
    options={'build_exe': options},
    executables=[target]
)
