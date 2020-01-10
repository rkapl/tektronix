from setuptools import setup

setup(name='tektronix',
      version='0.1',
      description='Tektronix Oscilloscope data acquisition tool',
      url='http://github.com/rkapl/tektronix',
      author='Roman Kapl',
      author_email='code@rkapl.cz',
      license='GPLv2',
      packages=['tektronix'],
      scripts=['bin/tektronix'],
      zip_safe=False)