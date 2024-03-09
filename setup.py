from setuptools import setup, find_packages

setup(
    name="annotate-with-microdata",
    version="0.1",
    author="Timur Ibragimov",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["microdata = src.cli:main"]
    }
)