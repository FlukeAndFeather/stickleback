import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="stickleback",
    version="0.1.1",
    description="Automated behavioral event detection in bio-logging data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="http://github.com/FlukeAndFeather/stickleback",
    author="Max Czapanskiy",
    author_email="maxczapanskiy@gmail.com",
    license="MIT",
    packages=['stickleback'],
    include_package_data=True,
    package_data={'stickleback': ['data/*']},
    install_requires=[
            "jupyter~=1.0",
            "matplotlib~=3.4",
            "netcdf4~=1.5",
            "numpy~=1.20",
            "pandas~=1.2",
            "plotly~=4.12",
            "scikit-learn~=0.24",
            "scipy~=1.6",
            "sktime~=0.8"
        ]
)
