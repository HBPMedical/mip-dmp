# MIP Dataset Mapper (`mip_dmp`)

Python tool with Graphical User Interface to map datasets to specific Common Data Elements (CDEs)metadata schema of a federation of the Medical Informatics Platform (MIP). It is developed to support members of a MIP Federation in the task of mapping their dataset to the CDEs schema of this federation. 

## How to install?

1. Clone the Git repository in your prefered directory:

```bash
$ cd "/prefered/directory"
$ git clone git@github.com:HBPMedical/mip-datatools.git
```

2. Go to the cloned repository and create a new virtual Python 3.9 environment:

```bash
$ cd mip-datatools
$ virtualenv venv -p python3.9
```

3. Activate the environment and install the package with Pip:

```bash
$ source ./venv/bin/activate
(venv) $ pip install -e .
```

## Usage

### `mip_dataset_mapper_ui `

You can use the installed `mip_dataset_mapper_ui ` script to start the MIP Dataset Mapper UI application.

**Usage**

In a terminal, you can launch it with the following command:
```
$ mip_dataset_mapper_ui 
```

This will display a window that consists of four main component in grid layout fashion.

The task of mapping the dataset would consist of the following tasks:

- Load a input CSV dataset in `.csv` format (top left)
- Load a CDEs schema in `.xlxs` format (bottom left)
- Edit the columns / CDEs mapping table (top right)
- Configure output directory / filename and create the output CSV dataset mapped to the CDEs schema (bottom right)
