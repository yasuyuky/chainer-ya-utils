from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chainer_ya_utils',
    version='0.1.0',
    description='Yet Another Utilities for Chainer',
    long_description=long_description,
    url='https://github.com/yasuyuky/chainer-ya-utils',
    author='Yasuyuki YAMADA',
    author_email='yasuyuki.ymd@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='chainer',
    packages=['chainer.ya.utils'],
    install_requires=['chainer', 'requests'],
)
