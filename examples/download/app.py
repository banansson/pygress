#!/usr/bin/python

import sys
import time
sys.path.append('../../src')
from pygress import *
from webclient import WebClient

def run_download(components, size):
  bar = ProgressBar(components, size)
  for n in range(100, size + 1, 50):
    bar.update(n)
    time.sleep(0.005)
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
	[Label("some.file.with.a.long.name.that.need.to.be.capped"), Remaining(), Bar(), Percentage()],
        [Label("some.file", 32), Remaining(), Bar(), Percentage()]]
    for c in components:
      run_download(c, int(args[2]))

    print("--> done")
    exit()

  url = sys.argv[1]
  client = WebClient(ProgressBarFactory())

  try:
      client.get(url)
  except KeyboardInterrupt:
    print("\nUser canceled download")

