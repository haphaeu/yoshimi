from setuptools import setup, find_packages

setup(
        name='data_analysis',
        version='0.0.1',
        url='www.github.com/benhoff/data-analysis',
        license='BSD',
        author='Ben Hoff',
        packages=find_packages(),
        #install_requires=['PyQt5', 'pandas', 'sqlalchemy', 'nltk', 'numpy', 'jupyter', 'PyQtChart', 'lda', 'matplotlib', 'scipy', 'tweepy'],
        install_requires=['pandas', 'sqlalchemy', 'nltk', 'numpy', 'jupyter', 'matplotlib', 'scipy', 'tweepy'],
        entry_points={},
        extras_require={'dev': ['flake8',]},
        )
