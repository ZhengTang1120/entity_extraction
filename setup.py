#setup.py
from distutils.core import setup, Extension
faerie_mod = Extension('faerie', sources = ['faerie.c'])
setup(name = "faerie",
    version = "0.1",
    description = "A implementation of faerie alg",
    author="Zheng Tang",
    ext_modules = [faerie_mod],
)