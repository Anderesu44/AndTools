from setuptools import setup, find_packages

setup(
    name="AndTools",
    version="1.7.0",
    packages=find_packages(),
    # install_requires=[],# Add your project dependencies here
    author="Andev",
    author_email="andev@gmail.com",
    description="Andev Tools is a collection of utilities for Python development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    python_requires=">=3.13",
)