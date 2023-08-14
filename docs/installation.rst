.. _installation:

***********************************
Installation Instructions for Users
***********************************

`mip_dmp` is a Python package that can easily be installed using `pip`.

1. Create your installation directory, go to this directory, and create a new virtual Python 3.9 environment::

    $ mkdir -p "/installation/directory"
    $ cd "/prefered/directory"
    $ virtualenv venv -p python3.9

2. Activate the environment and install the package, at a specific version, directly from GitHub with Pip::

    $ source ./venv/bin/activate
    (venv)$ pip install -r https://raw.githubusercontent.com/HBPMedical/mip-dmp/main/requirements.txt
    (venv)$ pip install git+https://github.com/HBPMedical/mip-dmp.git@0.0.7

.. note::
    `mip_dmp` has not been made available on the Python Package Index (PyPI) yet, so we need to install it directly from GitHub.
