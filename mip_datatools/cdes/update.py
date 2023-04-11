"""Module for updating the CDEs."""

import logging


def replace_chars(in_str, old_chars, new_chars):
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
        if out_str != in_str:
            logging.info(f"-> Change: {in_str} -> {out_str}")
    return out_str


def replace_characters_in_given_keys(
    in_dict,
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
    """
    out_dict = in_dict.copy()
    try:
        for k in keys:
            if " " not in in_dict[k]:  # Replace only if no space in string
                if exceptions is not None and in_dict[k] not in exceptions:
                    out_dict[k] = replace_chars(in_dict[k], old_chars, new_chars)
        return out_dict
    except Exception as e:
        logging.warning(f"Exception raised: {e}")
        return dict({})


def recursive_replace_dashes_and_underscores(cdes_data):
    """Replace the dashes and underscores in the name and code of CDEs' groups.

    Parameters
    ----------
    cdes_data : dict
        Dictionary loaded from CDEs file in JSON format.

    Returns
    -------
    cdes_data : dict
        Updated output dictionary describing the CDEs fpr the given federation.
    """
    STRING_EXCEPTIONS = ["FDG-PET", "follow-up", "Past-surgery", "Video-EEG"]
    if isinstance(cdes_data, dict):
        keys = cdes_data.keys()
        if ("label" in keys) and ("code" in keys):
            cdes_data = replace_characters_in_given_keys(
                cdes_data,
                old_chars=["-", "_"],
                new_chars=[" ", " "],
                keys=["code", "label"],
                exceptions=STRING_EXCEPTIONS,
            )
        if "groups" in keys:
            for i, item in enumerate(cdes_data["groups"]):
                cdes_data["groups"][i] = recursive_replace_dashes_and_underscores(item)
        return cdes_data
