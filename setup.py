from distutils.core import setup
import os, sys, glob

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name="dateevent",
      scripts=['dateevent'],
      version='0.2.1',
      maintainer="Gabriel Boehme and Boris Pohler",
      maintainer_email="m.gabrielboehme@googlemail.com",
      description="DateEvent",
      long_description=read('dateevent.longdesc'),
      data_files=[('share/applications',['dateevent.desktop']),
                  ('bin/',['dateevent_daemon']),
                  ('share/applications',['splash.jpg']),
                  ('share/icons/hicolor/64x64/apps', ['dateevent.png']),
                  ('share/dateevent/img', ['dateeventsplash.jpg']),
                  ('share/dateevent/qml', glob.glob('qml/*.*')),
                  ('share/dateevent/img', glob.glob('img/*.png')),
                  ('share/dateevent',['daemon.py']),
                  ('share/dateevent',['eventfeed.py']),],)
