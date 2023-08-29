from setuptools import setup, find_packages

setup(
    name="GeneticML",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "loguru",
        "tiktoken",
        "bs4",
        "requests",
        "git+https://github.com/locomotive-agency/taxonomyml.git",
    ],
    author="jroakes@gmail.com",
    description="Automatically refine Python code to meet specified objectives.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jroakes/GeneticML",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
