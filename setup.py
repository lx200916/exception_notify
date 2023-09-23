from setuptools import setup, find_packages
setup(
    name="exception_notify",
    version="0.4",
    author="SaltedFish",
    packages=find_packages(),
    install_requires=[
    "requests",
    "tomli"
    ]
)