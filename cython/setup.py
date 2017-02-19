from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("test_cython_c.pyx")
)