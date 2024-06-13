from setuptools import setup, find_packages
from os import path

with open(path.join(path.dirname(__file__), "description.md"), "r") as file:
    description = file.read()

setup(
    name="fletmint",
    version="0.1.6.1",
    author="Edoardo Balducci",
    author_email="edoardoba2004@gmail.com",
    description="A sharp and modern components library for Flet",
    long_description=description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["flet"],
    python_requires=">=3.8",
    project_urls={
        "support": "https://www.patreon.com/edoardobalducci",
        "repository": "https://github.com/Bbalduzz/fletmint",
        "tracker": "https://github.com/Bbalduzz/fletmint/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
