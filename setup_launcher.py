import os, subprocess, sys
root=os.path.dirname(os.path.abspath(__file__))
subprocess.call(['cmd','/c',os.path.join(root,'setup.bat')])
