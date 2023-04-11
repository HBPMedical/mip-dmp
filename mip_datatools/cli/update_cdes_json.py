"""Standalone script which updates the CDEs of the federations of the Medical Informatics Platform (MIP)."""

import sys
from argparse import ArgumentParser
from pathlib import Path
import json
import logging


VALID_COMMANDS = ["remove_dashes_and_underscores"]


def create_parser():
    """Create argument parser of the script.

    Returns
    -------
    p : argparse.ArgumentParser
        Parser of the script.
    """
    p = ArgumentParser(
        description="Script to remove dashes and underscores in the handsons CDEs."
    )
    p.add_argument(
        "--cdes_file",
        required=True,
        help="Common data elements (CDEs) file in JSON format.",
    )
    p.add_argument(
        "--command",
        required=True,
        choices=VALID_COMMANDS,
        help="Command to be performed on the CDEs.",
    )
    p.add_argument(
        "--output_json_suffix",
        required=False,
        default="corrected",
        help="Suffix added to the original name for the output CDEs in JSON format.",
    )
    p.add_argument(
        "--output_json_indent",
        required=False,
        default=4,
        help="Indent to use for writing the output CDEs file.",
    )
    p.add_argument(
        "--log_file",
        required=False,
        default=None,
        help="Path to output log file. "
        "If not provided, the log file will be saved in the same directory "
        "as the CDEs file with the name `cdes_update.log`.",
    )
    return p


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
    out_str = in_str.copy()
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


def setup_logging(log_file):
    """Set up logging.

    Parameters
    ----------
    log_file : str
        Path to output log file.
    """
    logging.basicConfig(
        filename=log_file,
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )


def main():
    """Main script function.

    Returns
    -------
    exit_code : {0, 1}
        Exit code (0: success / 1: error)
    """
    # Create parser and parse script arguments
    parser = create_parser()
    args = parser.parse_args()

    # Set path of log file
    log_file = (
        args.log_file
        if args.log_file is not None
        else (Path(args.cdes_file).parent / "cdes_update.log").absolute()
    )
    # Set up logging with log file
    setup_logging(log_file)

    # Log script arguments
    logging.info("Starting script with arguments: %s", args)

    # Load the CDEs
    cdes_data = load_cdes(args.cdes_file)

    # Replace "-" and "_" characters by white space
    if args.command == "remove_dashes_and_underscores":
        cdes_data = recursive_replace_dashes_and_underscores(cdes_data)

    # Write edited CDEs to json file
    in_cdes_fname = Path(args.cdes_file)
    out_cdes_fname = in_cdes_fname.parent / (
        "_".join([in_cdes_fname.stem, args.output_json_suffix]) + ".json"
    )
    write_cdes(cdes_data, out_cdes_fname, indent=args.output_json_indent)
    logging.info(
        ["Done writing", out_cdes_fname, "with indent =", args.output_json_indent]
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
