from setuptools import setup, find_packages

setup(
    name="benchmark-reliability",
    version="0.1.7",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "brf.registry": ["manifest.yaml"],
    },
    install_requires=[
        "numpy>=1.18",
        "scikit-learn>=0.24",
        "pandas>=1.1",
        "scipy>=1.5",
        "openml>=0.12",
    ],
    entry_points={
        "console_scripts": [
            "brf=brf.cli:main",
        ],
    },
)
