
#!/usr/bin/python
from subprocess import Popen
import sys

filename = 'downloadVideo.py'
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()