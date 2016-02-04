from distutils.core import setup
setup(
  name = 'faerie',
  packages = ['faerie'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Zheng Tang',
  author_email = 'zhengtan@isi.edu',
  url = 'https://github.com/ZhengTang1120/entity_extraction/faerie', # use the URL to the github repo
  keywords = ['heap', 'entity_extraction'], # arbitrary keywords
  classifiers = [
  	# How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',
    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: C',
  ],
)