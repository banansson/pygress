#!/usr/bin/python

import sys
import math

class ProgressBarFactory:

  def create(self, components, size):
    return ProgressBar(components, size)

  def create_default(self, size):
    return ProgressBar([Percentage(), Bar()], size)

class ProgressBarComponent(object):

  def update(self, progress):
    pass

  def render():
    pass

class Percentage(ProgressBarComponent):

    def __init__(self):
      self.output = 0

    def update(self, progress):
      self.outout = progress.progress * 100

    def render(self):
      return "%3.0f%%" % self.outout

class Bar(ProgressBarComponent):

    def __init__(self):
      self.output = 0

    def update(self, progress):
      count = int(math.ceil(progress.progress * 25))
      self.output = ''.join(['=' for num in xrange(count)])

    def render(self):
      return "[%-25s]" % self.output

class Remaining(object):

  def __init__(self):
    self.size = 0
    self.output = 0

  def update(self, progress):
    reverse_progress = 1 - progress.progress
    self.size = reverse_progress * progress.size

  def render(self):
    (self.output, postfix) = self._scale(self.size)
    return "%4d %-2s" % (self.output, postfix)

  def _scale(self, size):
    kilobyte = 1024
    megabyte = kilobyte * 1024
    terabyte = megabyte * 1024
    petabyte = terabyte * 1024

    if (size < kilobyte):
      return (size, 'B')
    if (size < megabyte):
      return (size / kilobyte, 'kB')
    if (size < terabyte):
      return (size / megabyte, 'MB')
    if (size < petabyte):
      return (size / terabyte, 'GB')

class ProgressBar:

  def __init__(self, components, size, out=sys.stderr):
    self.size = size
    self.current = 0
    self.last_known = 0
    self.progress = 0
    self.out = out
    self.components = components

  def update(self, current):
    self.current = current
    if not self._update_required() or self.done():
      return

    self.last_known = current
    self.progress = current / float(self.size)

  def render(self):
    percent = self.progress * 100
    row = ''
    for i, c in enumerate(self.components):
      c.update(self)
      row += c.render() + ' '

    self._write(row)
    if self.done():
      self._write("\n")

  def done(self):
    return self.progress == 1

  def _update_required(self):
    return self.last_known != self.current

  def _write(self, output):
    self.out.write("\r" + output)
    self.out.flush()

