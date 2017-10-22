#!/usr/bin/python

from http import client
from urllib.parse import urlparse

class WebClient:

  def __init__(self, factory):
    self.pbf = factory

  def _get_url_details(self, url):
    u = urlparse(url)
    host = u.netloc
    path = u.path
    file_name = u.path.split('/')[-1]
    return (host, path, file_name)

  def _make_connection(self, host, path):
    connection = client.HTTPConnection(host)
    connection.request('GET', path)
    return connection

  def get(self, url):
    (host, path, file_name) = self._get_url_details(url)

    if path == '/':
      file_name = 'temp.file'

    connection = self._make_connection(host, path)
    response = connection.getresponse()

    if (response.status == 302):
      connection.close()
      url = response.getheader('Location')
      print('Redirect (304) to %s' % url)
      (host, path, file_name) = self._get_url_details(url)
      connection = self._make_connection(host, path)
      response = connection.getresponse()

    if (response.status != 200):
      print('Got {} {}, expected 200 OK or 302 FOUND'.format(response.status, response.reason))
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
