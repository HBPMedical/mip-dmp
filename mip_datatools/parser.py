"""Module to create argument parser of the script, i.e. command line interface."""

from argparse import ArgumentParser


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
        "--cdes_json_file",
        required=True,
        help="Common data elements (CDEs) file in JSON format.",
    )
    p.add_argument(
        "--cdes_excel_file",
        required=True,
        help="Common data elements (CDEs) file in EXCEL format.",
    )
    p.add_argument(
        "--command",
        required=True,
        choices=VALID_COMMANDS,
        help="Command to be performed on the CDEs.",
    )
    p.add_argument(
        "--output_dir",
        required=False,
        default="None",
        help="Directory where the output CDEs files will be saved. "
        "If not provided, the output files will be saved in the same directory as the CDEs JSON file.",
    )
    p.add_argument(
        "--output_suffix",
        required=False,
        default="corrected",
        help="Suffix added to the original name for the output CDEs in JSON or EXCEL format.",
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
