#!/usr/bin/python

import sys
import math
import time

class ProgressBarFactory(object):

  def create(self, components, size):
    return ProgressBar(components, size)

  def create_default(self, size):
    return ProgressBar([Percentage(), Bar()], size)

  def create_file_download(self, name, size):
    return self.create([Label(name), Remaining(), Bar(), Speed(), Percentage()], size)

class ProgressBarComponent(object):

  def update(self, progress):
    pass

  def render():
    pass

class Label(ProgressBarComponent):

  def __init__(self, text, max_chars=32):
    self.max_chars = max_chars
    self.output = self._format(text)

  def _format(self, text):
    full_format = "{0:{width}s}".format(text, width=self.max_chars)
    capped_format = "{0:s}...".format(text[0:self.max_chars - 3])

    return full_format if len(text) <= self.max_chars else capped_format

  def render(self):
    return self.output

class Percentage(ProgressBarComponent):

    def __init__(self):
      self.output = 0

    def update(self, progress):
      self.outout = progress.progress * 100

    def render(self):
      return "%3.0f%%" % self.outout

class Bar(ProgressBarComponent):

  def __init__(self, background='-', tick='#'):
    self.background = background
    self.tick = tick
    self.size = 32
    self.output = 0

  def update(self, progress):
    count = int(math.ceil(progress.progress * self.size))
    done = ''.join([self.tick for num in range(count)])
    left = ''.join([self.background for num in range(self.size - len(done))])
    self.output = done + left

  def render(self):
    form = "[%-{:d}s]".format(self.size)
    return form % self.output

class Remaining(ProgressBarComponent):

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

class Speed(ProgressBarComponent):

    def __init__(self):
      self.speed = 0
      self.previous_progress = 0
      self.previous_timestamp = time.time()

    def update(self, progress):
      now = time.time()
      time_delta = now - self.previous_timestamp
      progress_delta = (progress.progress * progress.size) - self.previous_progress

      self.speed = progress_delta / time_delta
      self.previous_timestamp = now
      self.previous_progress = progress.progress * progress.size

    def render(self):
        return "%.2f MB/s" % (self.speed / (1024 * 1024))

class ProgressBar:

  def __init__(self, components, size, out=sys.stderr):
    self.size = size
    self.current = 0
    self.last_known = 0
    self.progress = 0
    self.out = out
    self.components = components
    self.last_render = 0

  def update(self, current):
    self.current = current
    self.last_known = current
    self.progress = current / float(self.size)

  def render(self):
    now = time.time()
    percent = self.progress * 100
    row = ''
    for i, c in enumerate(self.components):
      c.update(self)
      row += c.render() + ' '

    if now - self.last_render > 0.1:
      self._write(row)
      self.last_render = now

    if self.done():
      self._write("\n")

  def done(self):
    return self.progress == 1

  def _update_required(self):
    return self.last_known != self.current

  def _write(self, output):
    self.out.write("\r" + output)
    self.out.flush()
