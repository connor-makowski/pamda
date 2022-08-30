from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'pamda',
  packages = ['pamda'],
  version = '0.0.14',
  license='MIT',
  description = 'Python wrapper of object oriented processes for functional programming styles similar to Ramda',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Connor Makowski',
  author_email = 'connor.m.makowski@gmail.com',
  url = 'https://github.com/connor-makowski/pamda',
  download_url = 'https://github.com/connor-makowski/pamda/dist/pamda-0.0.14.tar.gz',
  keywords = ['data', 'ramda', 'pamda','functional'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
