# Copyright 2023 The HIP team, University Hospital of Lausanne (CHUV), Switzerland & Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for input/output operations with files involved in the MIP Dataset Mapper."""

import json
from pathlib import Path
import pandas as pd
import gensim.downloader as api
import chars2vec

from mip_dmp.process.mapping import MAPPING_TABLE_COLUMNS


def load_csv(csc_file: str):
    """Load content of a CSV file.

    Parameters
    ----------
    csv_file : str
        Path to CSV file.

    Returns
    -------
    data : pd.DataFrame
        Dataframe loaded from CSV file.
    """
    data = pd.read_csv(csc_file)
    return data


def load_excel(excel_file: str):
    """Load content of an Excel file.

    Parameters
    ----------
    excel_file : str
        Path to Excel file.

    Returns
    -------
    data : pd.DataFrame
        Dataframe loaded from Excel file.
    """
    data = pd.read_excel(excel_file)
    return data


def load_json(json_file: str):
    """Load content of a JSON file.

    Parameters
    ----------
    json_file : str
        Path to JSON file.

    Returns
    -------
    data : dict
        Dictionary loaded from JSON file.
    """
    with open(json_file) as f:
        data = json.load(f)
        return data


def load_mapping_json(json_file: str):
    """Load content of a saved mapping JSON file.

    Parameters
    ----------
    json_file : str
        Path to JSON file.

    Returns
    -------
    data : dict
        Dictionary loaded from JSON file.
    """
    data = pd.read_json(json_file, orient="records")
    # Check if the mapping file is in the correct format
    # i.e. if it contains the required columns listed in
    # MAPPING_TABLE_COLUMNS
    if not all([col in data.columns for col in MAPPING_TABLE_COLUMNS]):
        raise ValueError(
            "The mapping file is not in the correct format. "
            "The mapping file must contain the following columns: "
            f"{MAPPING_TABLE_COLUMNS}."
        )
    return data


def generate_output_path(input_cdes_file: str, output_dir: str, output_suffix: str):
    """Generate output path for CDEs file, but without any extension.

    Parameters
    ----------
    input_cdes_file : str
        Path to input CDEs file in JSON or EXCEL format.

    output_dir : str
        Path to directory where the output CDEs file will be written.

    output_suffix : str
        Suffix to add to the input CDEs file name, to generate the output CDEs file name.

    Returns
    -------
    out_cdes_fname : str
        Generated absolute path for the output CDEs files where the updated CDEs are written, with
        extension automatically added (.json for JSON, .xlsx for EXCEL).
    """
    in_cdes_fname = Path(input_cdes_file)
    out_cdes_fname = Path(output_dir) / (
        "_".join([in_cdes_fname.stem, output_suffix]) + in_cdes_fname.suffix
    )
    return out_cdes_fname.absolute()


def load_glove_model(model_name="glove-wiki-gigaword-50"):
    """Load a GloVe model from disk.

    Parameters
    ----------
    model_name : str, optional
        Name of the GloVe model to load, by default "glove-wiki-gigaword-50"

    Returns
    -------
    dict
        Dictionary containing the GloVe model.
    """
    return api.load(model_name)


def load_c2v_model(model_name="eng_50"):
    """Load a chars2vec model from disk.

    Parameters
    ----------
    model_name : str, optional
        Name of the chars2vec model to load, by default "eng_50"

    Returns
    -------
    dict
        Dictionary containing the chars2vec model.
    """
    return chars2vec.load_model(model_name)
