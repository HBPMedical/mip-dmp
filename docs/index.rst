Welcome to the documentation of MIP Dataset Mapper (`mip_dmp`)!
=================================================================

This tool is developed by the MIP team at the University Hospital of Lausanne (CHUV) for use within the lab, as well as for open-source software distribution.

.. image:: https://img.shields.io/github/v/release/HBPMedical/mip-dmp
  :alt: Latest GitHub Release
.. image:: https://img.shields.io/github/release-date/HBPMedical/mip-dmp
  :alt: GitHub Release Date
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.8056371.svg
  :target: https://doi.org/10.5281/zenodo.8056371
  :alt: Digital Object Identifier (DOI)
.. image:: https://github.com/HBPMedical/mip-dmp/actions/workflows/python-app.yml/badge.svg
  :target: https://github.com/HBPMedical/mip-dmp/actions/workflows/python-app.yml
  :alt: CI/CD


.. TODO add badge for maybe docs 

Introduction
-------------

`mip_dmp` is an open-source tool written in Python with Command-line and Graphical User Interfaces to map datasets to a specific Common Data Elements (CDEs) metadata schema of a federation of the Medical Informatics Platform (MIP). It is developed to support members of a MIP Federation in the task of mapping their dataset to the CDEs schema of this federation.

Aknowledgment
--------------

If your are using `mip_dmp` in your work, please acknowledge this software and its dependencies. See :ref:`Citing <citing>` for more details.

License information
--------------------

This software is distributed under the open-source Apache 2.0 license. See :ref:`license <LICENSE>` for more details.

All trademarks referenced herein are property of their respective holders.

Help/Questions
---------------

If you run into any problems or have any code bugs or questions, please create a new `GitHub Issue <https://github.com/HBPMedical/mip-dmp/issues>`_.

Eager to contribute?
---------------------

See :ref:`Contributing <contributing>` for more details.

Funding
--------

This project received funding from the European Union's H2020 Framework Programme for Research and Innovation under the Specific Grant Agreement No. 945539 (Human Brain Project SGA3, as part the Human Intracerebral EEG Platform (HIP)).

Contents
=========

.. _getting_started:

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   installation

.. _user-docs:

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   cmd_usage
   ui_user_guide

.. _developer-docs:

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   developer

.. _api-doc:

.. toctree::
   :maxdepth: 5
   :caption: API Documentation

   api_cli_subpackage
   api_plot_subpackage
   api_process_subpackage
   api_qt5_subpackage
   api_gui_subpackage
   api_utils_subpackage

.. _about-docs:

.. toctree::
   :maxdepth: 1
   :caption: About mip_dmp

   LICENSE
   citing
   contributing
