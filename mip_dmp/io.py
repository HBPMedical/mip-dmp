"""Module for input/output operations."""

import json
from pathlib import Path
import pandas as pd


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
    out_cdes_fname_ : str
        Generated absolute path for the output CDEs files where the updated CDEs are written, with
        extension automatically added (.json for JSON, .xlsx for EXCEL).
    """
    in_cdes_fname = Path(input_cdes_file)
    out_cdes_fname = Path(output_dir) / (
        "_".join([in_cdes_fname.stem, output_suffix]) + in_cdes_fname.suffix
    )
    return out_cdes_fname.absolute()
