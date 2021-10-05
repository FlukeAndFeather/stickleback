from setuptools import setup, find_packages


setup(
    name="stickleback",
    description="Detect point behaviors in longitudinal sensor data",
    author="Max Czapanskiy",
    packages=find_packages(exclude=['notebooks']),
    package_data={'stickleback': ['data/*']}
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
