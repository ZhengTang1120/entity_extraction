from distutils.core import setup
from setuptools import Extension,find_packages
setup(
  name = 'faerie',
  version = '0.0.2',
  description = 'Dictionary-based entity extraction with efficient filtering',
  author = 'Zheng Tang',
  author_email = 'zhengtan@isi.edu',
  url = 'https://github.com/ZhengTang1120/entity_extraction/', # use the URL to the github repo
  packages = find_packages(),
  keywords = ['heap', 'entity_extraction'], # arbitrary keywords
  ext_modules=[Extension(
        'singleheap',
        ['singleheap.c'])]
)