from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='jupyter-snippets',

    version='0.3',
    
    python_requires='>3.7',

    description='Useful jupyter startup/initialisation snippets',
    long_description=long_description,

    url='https://github.com/hottwaj/jupyter-snippets',

    author='Jonathan Clarke',
    author_email='jonathan.a.clarke@gmail.com',

    license='Copyright 2020',

    classifiers=[
    ],

    keywords='',

    packages=["jupyter_snippets"],
    
    install_requires=[
        "matplotlib",
        "seaborn",
        "ipython",
        "notebook",
        'beautifulsoup4'
    ],
)
