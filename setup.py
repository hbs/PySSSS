from setuptools import setup, find_packages
from pyssss import __version__, __author__

if __name__ == '__main__':
    project_name = "full_text_rss"
    setup(
        name=project_name,
        version=__version__,
        author=__author__,
        license="Apache Software License",
        url="https://github.com/hbs/PySSSS",
        packages=find_packages(),
        long_description=open('README').read(),
    )
