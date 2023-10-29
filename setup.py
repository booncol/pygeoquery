from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pygeoquery",
    version="0.1.3",
    description="Geoqueries on Firestore Database for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lukasz Majda",
    author_email="lukasz.majda@gmail.com",
    license="MIT",
    keywords="firestore geoquery geospatial geofire geohash",
    url="https://github.com/booncol/pygeoquery",
    package_dir={"pygeoquery": "pygeoquery"},
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "geohashr==1.3.1",
        "geopy==2.4.0",
        "google-cloud-firestore==2.13.0",
    ]
)
