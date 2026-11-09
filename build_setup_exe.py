"""Optional Windows helper: creates setup.exe with PyInstaller.
Run: pip install pyinstaller && python build_setup_exe.py
"""
import PyInstaller.__main__
PyInstaller.__main__.run(['--onefile','--name','MediCare_Setup','setup_launcher.py'])
