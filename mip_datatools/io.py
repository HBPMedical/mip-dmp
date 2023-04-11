"""Module for input/output operations."""

import json


def load_cdes(cdes_file):
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


def write_cdes(cdes_data, out_cdes_fname, **kwargs):
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
