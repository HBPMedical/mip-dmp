# mip_datatools

Python tools to manipulate Metadata schema of Common Data Elements for the federations of the Medical Informatics Platform (MIP). 

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

## How to use the installed scripts?

### `mip_update_cdes_json`

Script to update the CDES JSON/EXCEL file pair to make this process more reproducible. 

**Usage**

In a terminal, you can run it with the folllowing command:
```
$ mip_update_cdes_json \
    --cdes_json_file "/path/to/CDEsMetadata.json" \
    --cdes_excel_file "/path/to/myCDEs.xlxs" \
    --command "remove_dashes_and_underscores" \
    --output_suffix "updated" \
    --log_file "/path/to/CDEs_update.log" 
```
**Note:** You can use the option `-h`to show more details about usage documentation.

Available commands:

- `remove_dashes_and_underscores`: Remove dashes and underscores.

### `mip_dataset_mapper_ui `

Script to start the MIP Dataset Mapper UI, a tool to support members of a MIP Federation in the task of mapping their dataset to the Common Data Elements schema of the MIP Federation.

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
