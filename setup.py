from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='fragplot',
    version='0.0',
    description=readme().split('\n')[1],
    url='http://github.com/elhb/fragplot',
    author='Erik Borgstroem',
    author_email='erik.borgstrom@scilifelab.se',
    packages=['fragplot'],
    install_requires=['matplotlib'],
    scripts=['script/fragplot']
    )

