#!/usr/bin/python

import sys
import time
sys.path.append('../../src')
from pygress import *
from webclient import WebClient

def run_download(components, size):
  size = size * 1024 * 1024 # Size in MB
  speed = 10 # Spee to aim for in MB/s
  wait = 0.1 # Faking a network
  chunk = int((1024 * 1024 * speed) * wait) # Fake speed by progressing a certain amount
  bar = ProgressBar(components, size)
  for n in range(0, size + 1, chunk):
    bar.update(n)
    time.sleep(wait)
    bar.render()

def usage(me):
  print("usage: %s [<file>|fake <size>]" % me)

if __name__ == '__main__':

  if len(sys.argv) < 2:
    print("It would help if you specified what I'm supposed to download :)")
    print(usage(sys.argv[0]))
    exit(0)

  args = sys.argv

  if args[1] == "fake":
    print("--> faking download")
    if not len(args) == 3:
      print(" -> can't fake without a value")
      exit()

    components = [
      [Label("some.file"), Remaining(), Speed(), Bar(), Percentage()],
    ]
    for c in components:
      run_download(c, int(args[2]))

    exit()

  url = sys.argv[1]
  client = WebClient(ProgressBarFactory())

  try:
      client.get(url)
  except KeyboardInterrupt:
    print("\nUser canceled download")
