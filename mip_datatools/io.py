"""Module for input/output operations."""

import json
import logging
from pathlib import Path
from openpyxl import load_workbook, Workbook


def load_cdes_json(cdes_file: str):
    """Load content of a CDEs file (in JSON format).

    Parameters
    ----------
    cdes_file : str
        Path to CDEs file in JSON format.

    Returns
    -------
    cdes_data : dict
        Dictionary loaded from CDEs file (in JSON format).
    """
    with open(cdes_file) as f:
        cdes_data = json.load(f)
        return cdes_data


def write_cdes_json(cdes_data: dict, out_cdes_fname: str, **kwargs):
    """Write content of CDEs to JSON file.

    Parameters
    ----------
    cdes_data : dict
        Dictionary loaded from CDEs file in JSON format.

    out_cdes_fname : str
        Absolute path of file where the updated CDEs are written.

    **kwargs
        Additional keyword arguments passed to `json.dump()`.
    """
    with open(out_cdes_fname, "w") as f:
        json.dump(cdes_data, f, **kwargs)


def load_cdes_excel(cdes_file: str):
    """Load content of a CDEs file (in .xlsx format).

    Parameters
    ----------
    cdes_file : str
        Path to CDEs file in .xlsx format.

    Returns
    -------
    cdes_data : openpyxl.Workbook
        A openpyxl Workbook object loaded from CDEs file (in .xlsx format).
    """
    cdes_wb = load_workbook(cdes_file, data_only=True)
    return cdes_wb


def write_cdes_excel(cdes_wb: Workbook, out_cdes_fname: str):
    """Write content of CDEs to EXCEL file.

    Parameters
    ----------
    cdes_wb : openpyxl.Workbook
        A openpyxl Workbook object to save in .xlsx format.

    out_cdes_fname : str
        Absolute path of file where the updated CDEs are written.
    """
    cdes_wb.save(out_cdes_fname)


def write_cdes(cdes_data, cdes_wb, out_json_path, out_excel_path, out_json_indent=4):
    """ "Write content of CDEs to JSON and EXCEL file.

    Parameters
    ----------
    cdes_data : dict
        Dictionary describing CDEs to be written to JSON file.

    cdes_wb : openpyxl.Workbook
        A openpyxl Workbook object describing CDEs to be written to EXCEL file.

    out_json_path : str
        Absolute path of file where the updated CDEs are written in JSON format
        (.json extension).

    out_excel_path : str
        Absolute path of file where the updated CDEs are written in EXCEL format
        (.xlsx extension).

    out_json_indent : int, optional
        Indent to use for writing the output CDEs file in JSON format, by default 4.
    """
    # Write edited CDEs to json file
    write_cdes_json(cdes_data, out_json_path, indent=out_json_indent)
    logging.info(f"Done writing {out_json_path}, with indent = {out_json_indent}")
    write_cdes_excel(cdes_wb, out_excel_path)
    logging.info(f"Done writing {out_excel_path}")


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
