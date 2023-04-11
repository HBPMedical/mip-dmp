import setuptools

# This extracts the required packages from the requirements.txt file
with open("requirements.txt") as f:
    required = f.read().splitlines()

# This calls the setup function from setuptools
# with the list of required packages
setuptools.setup(install_requires=required)
