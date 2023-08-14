.. _instructions:

***************************
Instructions for Developers
***************************

.. _instructions_mip_dmp_install:

How to install `mip_dmp` locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important::
    `mip_dmp` requires a Python environment with `python>=3.9`.

1. Clone the original or your fork repository of `mip_dmp` and go to the clone directory::

    cd /path/to/directory/where/you/want/to/clone/mip_dmp
    git clone https://github.com/HBPMedical/mip-dmp
    cd mip-dmp

2. Install `mip_dmp` along with all dependencies::

    # Install main package dependencies
    pip install -r requirements.txt  
    # Install dependencies for development, including dependencies
    # to lint/format the code and to test the package
    pip install -r requirements-dev.txt
    # Install dependencies to build the documentation
    pip install -r docs/requirements.txt
    # Install mip_dmp in editable mode
    pip install -e .

.. _instructions_docs_build:

How to build the documentation locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install `mip_dmp` and its dependencies (see :ref:`instructions_mip_dmp_install`).

2. Go to the `docs` of the cloned repository and build the HTML documentation with `make`::

    cd docs
    make clean && make html

   The built HTML files of the documentation, including its main page (``index.html``), can be found in the ``docs/build/html`` directory, and can be opened in your favorite browser.

.. note::
	If you have made any changes in the `mip_dmp` docstrings, make sure to re-install `mip_dmp` prior to building the documentation by running ``pip install -e .``.
