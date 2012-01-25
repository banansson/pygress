#!/usr/bin/python

import sys
import math

class ProgressBarFactory:

  def create(self, size):
    return ProgBar(size)

class ProgBar:

  def __init__(self, size, out=sys.stderr):
    self.size = size
    self.current = 0
    self.last_known = 0
    self.progress = 0
    self.out = out

  def update(self, current):
    self.current = current
    if not self._update_required() or self.done():
      return

    self.last_known = current
    self.progress = current / float(self.size)

  def render(self):
    percent = self.progress * 100
    count = int(math.ceil(self.progress * 25))
    segments = ''.join(['=' for num in xrange(count)])
    bar = "%3.0f%% [%-25s] %d/%d" % (percent, segments, self.current, self.size)
    if not self.done():
      self._write(bar + "\r")
    else:
      self._write(bar + "\n")

  def done(self):
    return self.progress == 1

  def _update_required(self):
    return self.last_known != self.current

  def _write(self, output):
    self.out.write(output)
    self.out.flush()

