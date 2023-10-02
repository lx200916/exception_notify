from setuptools import setup, find_packages
setup(
    name="exception_notify",
    version="0.7.6",
    author="SaltedFish",
    packages=find_packages(),
    install_requires=[
    "requests",
    "tomli"
    ]
)