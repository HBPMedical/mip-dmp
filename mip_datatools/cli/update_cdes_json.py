"""Standalone script which updates the CDEs of the federations of the Medical Informatics Platform (MIP)."""

import sys
from pathlib import Path
import logging

from mip_datatools.io import load_cdes, write_cdes
from mip_datatools.parser import create_parser
from mip_datatools.logger import setup_logging
from mip_datatools.cdes.update import recursive_replace_dashes_and_underscores


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
    logging.info(f"Starting script with arguments: {args}")

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
        f"Done writing {out_cdes_fname}, with indent = {args.output_json_indent}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
