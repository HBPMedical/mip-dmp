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

## How to use the scripts?

### `mip_update_cdes_json`

```
$ mip_update_cdes_json \
    --cdes_file "/path/to/CDEsMetadata.json" \
    --command "remove_dashes_and_underscores" \
    --output_json_suffix "updated" \
    --log_file "/path/to/CDEs_update.log" 
```