#!/usr/bin/python

import sys
import time
from progbar import *
from webclient import WebClient

def usage(me):
  print "usage: %s [<file>|fake <size>]" % me

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "It would help if you specified what I'm supposed to download :)"
    print usage(sys.argv[0])
    exit()

  args = sys.argv

  if args[1] == "fake":
    print("--> faking download")
    if not len(args) == 3:
      print " -> can't fake without a value"
      exit()

    size = int(args[2])
    bar = ProgBar(size)
    for n in range(100, size + 1, 50):
      bar.update(n)
      time.sleep(0.005)
      bar.render()
    print "--> done"
    exit()

  url = sys.argv[1]
  client = WebClient(ProgressBarFactory())

  try:
      client.get(url) #, bar.render)
  except KeyboardInterrupt:
    print "\nUser canceled download"
