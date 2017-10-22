#!/usr/bin/python

from http import client
from urllib.parse import urlparse

class WebClient:

  def __init__(self, factory):
    self.pbf = factory

  def get(self, url):
    u = urlparse(url)
    host = u.netloc
    path = u.path
    file_name = u.path.split('/')[-1]

    if path == '/':
        file_name = 'temp.file'

    connection = client.HTTPConnection(host)
    connection.request('GET', u.path)
    response = connection.getresponse()
    if (response.status != 200):
        print("Got {} {}, expected 200 OK".format(response.status, response.reason))
        connection.close()
        return

    size = int(response.getheader("Content-Length"))
    target = open(file_name, "wb")
    bar = self.pbf.create_file_download(file_name, size)
    current = 0
    block_size = 8192
    while True:
      buffer = response.read(block_size)
      if not buffer:
        if current == size:
            bar.update(size)
            bar.render()
            print("Done: {} of {}".format(current, size))
        break

      target.write(buffer)
      current += len(buffer)
      bar.update(current)
      bar.render()

    connection.close()
