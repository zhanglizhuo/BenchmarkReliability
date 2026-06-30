from setuptools import setup, find_packages

setup(
    name="benchmark-reliability",
    version="0.1.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
