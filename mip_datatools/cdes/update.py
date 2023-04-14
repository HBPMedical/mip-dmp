"""Module for updating the CDEs."""

import logging
from openpyxl import Workbook
from openpyxl.utils import rows_from_range


STRING_EXCEPTIONS = [
    "FDG-PET",
    "follow-up",
    "Past-surgery",
    "Video-EEG",
    "Z-scores",
]


def replace_chars(in_str: str, old_chars: list, new_chars: list):
    """Replace a list of old and new characters in a string.

    Parameters
    ----------
    in_str : str
        Input string.

    old_chars : list
        List of characters to be replaced.

    new_chars : list
        List of new characters used as replacement.

    Returns
    -------
    out_str : str
        Updated string.
    """
    out_str = in_str
    for old_c, new_c in zip(old_chars, new_chars):
        out_str = new_c.join(out_str.split(old_c))
    return out_str


def replace_characters_in_given_keys(
    in_dict: list,
    in_wb: Workbook,
    old_chars=["-", "_"],
    new_chars=[" ", " "],
    keys=["code", "label"],
    exceptions=None,
):
    """Replace a list of old and new characters in the given keys of a dictionary.

    Parameters
    ----------
    in_dict : dict
        Input dictionary (describing the CDEs) to be updated.

    in_wb : openpyxl.Workbook
        Input workbook loaded from the CDEs in EXCEL format.

    old_chars : list
        List of characters to be replaced.

    new_chars : list
        List of new characters used as replacement.

    keys : list
        List of dictionary fields (keys) in which the characters are replaced.

    exceptions : list
        List of string exceptions which would not be modified.

    Returns
    -------
    out_dict : dict
        Updated dictionary describing the CDEs.
    out_wb : openpyxl.Workbook
        Updated workbook describing the CDEs.
    """
    out_dict = in_dict.copy()
    out_wb = in_wb
    try:
        for k in keys:
            if " " not in in_dict[k]:  # Replace only if no space in string
                if exceptions is not None and in_dict[k] not in exceptions:
                    out_dict[k] = replace_chars(in_dict[k], old_chars, new_chars)
                    if out_dict[k] != in_dict[k]:
                        logging.info(f"-> Change: {in_dict[k]} -> {out_dict[k]}")
                        out_wb = replace_chars_in_workbook(
                            in_wb, in_dict[k], out_dict[k]
                        )
        return (out_dict, out_wb)
    except Exception as e:
        logging.warning(f"Exception raised: {e}")
        return dict({}), None


def replace_chars_in_workbook(in_wb: Workbook, in_str: str, out_str: str):
    """Replace a string in a workbook.

    Parameters
    ----------
    in_wb : openpyxl.Workbook
        Input workbook loaded from the CDEs in EXCEL format.

    in_str : str
        Input string.

    out_str : str
        Output string.

    Returns
    -------
    out_wb : openpyxl.Workbook
        Updated workbook describing the CDEs.
    """
    # Copy the workbook
    out_wb: Workbook = in_wb

    # Select the sheet to modify
    sheet = out_wb.active

    # Loop through all the cells in the range and replace the string
    for row in rows_from_range(sheet.calculate_dimension()):
        for cell in row:
            if isinstance(cell, str) and cell is not None and in_str in cell:
                cell = out_str
    return out_wb


def recursive_replace_dashes_and_underscores(cdes_data, cdes_wb):
    """Replace the dashes and underscores in the name and code of CDEs' groups.

    Parameters
    ----------
    cdes_data : dict
        Dictionary loaded from CDEs file in JSON format.

    cdes_wb : openpyxl.Workbook
        Workbook loaded from the CDEs in EXCEL format.

    Returns
    -------
    cdes_data : dict
        Updated output dictionary describing the CDEs fpr the given federation.

    cdes_wb : openpyxl.Workbook
        Updated output workbook describing the CDEs for the given federation.
    """
    if isinstance(cdes_data, dict):
        keys = cdes_data.keys()
        if ("label" in keys) and ("code" in keys):
            cdes_data, cdes_wb = replace_characters_in_given_keys(
                cdes_data,
                cdes_wb,
                old_chars=["-", "_"],
                new_chars=[" ", " "],
                keys=["code", "label"],
                exceptions=STRING_EXCEPTIONS,
            )
        if "groups" in keys:
            for i, item in enumerate(cdes_data["groups"]):
                (
                    cdes_data["groups"][i],
                    cdes_wb,
                ) = recursive_replace_dashes_and_underscores(item, cdes_wb)
        return (cdes_data, cdes_wb)
    else:
        return (None, cdes_wb)
