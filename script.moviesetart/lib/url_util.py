import os, sys

if sys.version_info >= (3, 0):
  import urllib.request as urllib2
else:
  import urllib2

# URL utility methods from XBMC texture cache utility
# See https://github.com/MilhouseVH/texturecache.py
class UrlUtil(object):
  isPython3 = (sys.version_info >= (3, 0))

  # Convert quoted filename into consistent utf-8
  # representation for both Python2 and Python3
  @staticmethod
  def normalise(value, strip=False):
    if not value: return value

    v = urllib2.unquote(value)

    if strip:
      s = 8 if v.startswith("image://") else None
      if s:
        e = -1 if v[-1:] == "/" else None
        v = v[s:e]

    if not UrlUtil.isPython3:
      try:
        v = bytes(v.encode("iso-8859-1")).decode("utf-8")
      except UnicodeDecodeError:
        pass
      except UnicodeEncodeError:
        pass

    return v

  # Quote unquoted filename
  @staticmethod
  def denormalise(value, prefix=True):
    v = value

    if not UrlUtil.isPython3:
      try:
        v = bytes(v.encode("utf-8"))
      except UnicodeDecodeError:
        pass

    v = urllib2.quote(v, "")
    if prefix: v = "image://%s/" % v

    return UrlUtil.toUnicode(v)

  @staticmethod
  def toUnicode(data):
    if UrlUtil.isPython3: return data

    if isinstance(data, basestring):
      if not isinstance(data, unicode):
        try:
          data = unicode(data, encoding="utf-8", errors="ignore")
        except UnicodeDecodeError:
          pass

    return data