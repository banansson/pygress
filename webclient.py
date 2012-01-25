#!/usr/bin/python

import urllib2

class WebClient:

  def __init__(self, factory):
    self.pbf = factory

  def get(self, url):
    file_name = url.split('/')[-1]
    source = urllib2.urlopen(url)
    target = open(file_name, "wb")
    info = source.info()
    size = int(info.getheaders("Content-Length")[0])

    bar = self.pbf.create(size)
    current = 0
    block_sz = 8192
    while True:
      buffer = source.read(block_sz)
      if not buffer:
        break;

      target.write(buffer)
      current += len(buffer)
      bar.update(current)
      bar.render()

    target.close()

