from setuptools import setup, find_packages

setup(
    name="game_of_life",
    version="1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
