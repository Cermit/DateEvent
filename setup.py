from distutils.core import setup
import os, sys, glob

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name="dateevent",
      scripts=['dateevent'],
      version='0.1.0',
      maintainer="Gabriel Boehme and Boris Pohler",
      maintainer_email="email@example.com",
      description="A PySide example",
      long_description=read('dateevent.longdesc'),
      data_files=[('share/applications',['dateevent.desktop']),
                  ('share/applications',['dateevent_daemon']),
                  ('share/icons/hicolor/64x64/apps', ['dateevent.png']),
                  ('share/dateevent/qml', glob.glob('qml/*.*')),
                  ('share/dateevent/img', glob.glob('img/*.png')),
                  ('share/dateevent',['eventfeed.py']),],)
