.. _userguide:

***********************
Grahical User Interface
***********************

This page provides a user guide the MIP Dataset Mapper (``mip_dmp``) UI tool.

.. contents:: Table of Contents
    :local:
    :depth: 2

.. note::

    The UI is based on the `PySide2 <https://wiki.qt.io/Qt_for_Python>`_ Python binding for the `Qt <https://www.qt.io/>`_ cross-platform application framework.

0. Launch the UI
================

The UI can be launched by running the following command:

.. code-block:: console

    $ mip_dataset_mapper_ui

This will display the main window of the UI:

.. figure:: ./images/mip-dmp_ui_illustration_0.png
    :width: 100%
    :align: center

The UI is composed of 3 main parts:

-   The **menu bar** (at the top of the window) provides access to the different functionalities of the UI.
-   The **main window panel** (in the middle of the window) displays the different components of the UI:
    
    -   The **Source Dataset** component (on the top left) displays the content of the source dataset.
    -   The **Target CDEs Metadata Schema** component (on the bottom left) displays the content of the target Common Data Elements (CDEs) metatadata schema.
    -   The **Columns / CDEs Mapping** component (on the right) displays the different mappings between the columns of the source dataset and the CDEs of the target metadata schema, and provide mapping table row editor.

-   The **status bar** (at the bottom of the window) displays the status of the UI.

The different steps of the UI workflow are described in the following sections.

.. _load-source-dataset:

1. Load a source dataset
========================

The first step of the UI workflow is to load a source dataset. This can be done by clicking on the **Load CSV** button of the **Source Dataset** component of the menu bar:

.. figure:: ./images/mip-dmp_ui_illustration_1_1.png
    :width: 100%
    :align: center
|
This will open a file dialog window allowing to select a CSV file. Once a CSV file is selected, the content of the file is displayed in the **Source Dataset** component of the main window panel:

.. figure:: ./images/mip-dmp_ui_illustration_1_2.png
    :width: 100%
    :align: center

.. _load-target-cdes-metadata-schema:

2. Load a target CDEs metadata schema
======================================

The second step of the UI workflow is to load a target CDEs metadata schema. This can be done by clicking on the **Load XLXS** button of the **Target Schema** component of the menu bar:

.. figure:: ./images/mip-dmp_ui_illustration_2_1.png
    :width: 100%
    :align: center
|
This will open a file dialog window allowing to select a XLSX file. Once a XLSX file is selected, the content of the file is displayed in the **Target Schema** component of the main window panel:

.. figure:: ./images/mip-dmp_ui_illustration_2_2.png
    :width: 100%
    :align: center

.. _create-mappings:

3. Create the mappings
=======================

The third step of the UI workflow is to create the mappings between the columns of the source dataset and the CDEs of the target metadata schema. This can be done following (1) a manual or (2) a semi-automatic approach.

.. _create-mappings-manual:

3.1 Manual approach
--------------------

The manual approach consists in creating the mappings manually by clicking on the **Add** button below the table of the **Columns /CDEs Mappings** component of the menu bar:

.. figure:: ./images/mip-dmp_ui_illustration_3_1.png
    :width: 100%
    :align: center
|
This will open a dialog window allowing to select a column of the source dataset. A first matched CDE code is still proposed automatically by leveraging Fuzzy Text Matching from the `fuzzywuzzy <https://github.com/seatgeek/fuzzywuzzy>`_ Python library. A new row is then added to the table of the **Columns /CDEs Mappings** component and the user can edit the mapping (change the CDE code, define the transformation to apply to the column values, etc.) by using the **Mapping Row Editor**:

.. figure:: ./images/mip-dmp_ui_illustration_3_2.png
    :width: 100%
    :align: center

.. _create-mappings-semi-automatic:

3.2 Semi-automatic approach
----------------------------

The semi-automatic approach consists in initializing the mapping of all columns of the source dataset automatically by using one of three Natural Language Processing (NLP) methods (`fuzzy`, `glove`, `chars2vec`). The method can be selected from the dropdown list and then can be performed by clicking on the **Magic Stick** button of the **Mapping Initialization** component of the menu bar:

.. figure:: ./images/mip-dmp_ui_illustration_4_1.png
    :width: 100%
    :align: center
|
This will initialize the mapping of all columns of the source dataset automatically by leveraging the selected NLP method. The user can then edit the mapping (change the CDE code, define the transformation to apply to the column values, etc.) by using the **Mapping Row Editor**:

.. figure:: ./images/mip-dmp_ui_illustration_4_2.png
    :width: 100%
    :align: center

.. _check_mappings:

4. Check / Save the mappings
============================

The fourth step of the UI workflow is to check the mappings. This can be done by clicking on the **Check** button (magnifying glass) of the **Mapping (Load) / Check / Save** component of the menu bar:

.. figure:: ./images/mip-dmp_ui_illustration_5_1.png
    :width: 100%
    :align: center
|
This will check the mappings and display the result in a pop-up window:

.. figure:: ./images/mip-dmp_ui_illustration_5_2.png
    :width: 100%
    :align: center

Once the mappings of the table are validated, the fourth step of the UI workflow is to save the mappings. This can be done by clicking on the **Save JSON** button of the **Columns /CDEs Mappings** component of the menu bar:

.. figure:: ./images/mip-dmp_ui_illustration_6_1.png
    :width: 100%
    :align: center
|
This will open a file dialog window allowing to select a JSON file. Once a JSON file is selected, the mappings are saved in the file, and the result is displayed in a pop-up window:

.. figure:: ./images/mip-dmp_ui_illustration_6_2.png
    :width: 100%
    :align: center

This file can be then used by both the commandline and the UI applications of the MIP Dataset Mapper (``mip_dataset_mapper`` and ``mip_dataset_mapper_ui``).

.. _map_dataset:

5. Map a dataset
================

Once the mappings are saved / loaded, the user can map a dataset by clicking on the button of the **Map** component of the menu bar:

.. figure:: ./images/mip-dmp_ui_illustration_7_1.png
    :width: 100%
    :align: center
|
This will open a file dialog window allowing to select a CSV file. Once a CSV file is selected, the source dataset is mapped and the result status is displayed in status bar of the window:

.. figure:: ./images/mip-dmp_ui_illustration_7_2.png
    :width: 100%
    :align: center

.. note:
    Once the mappings are saved, the user can map a dataset just by using the commandline application of the MIP Dataset Mapper (``mip_dataset_mapper``). See the :ref:`cmdusage` section for more details.
