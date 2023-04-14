"""Standalone script which updates the CDEs of the federations of the Medical Informatics Platform (MIP)."""

import sys
from pathlib import Path
import logging

from mip_datatools.io import (
    load_cdes_json,
    write_cdes_json,
    load_cdes_excel,
    generate_output_path,
    write_cdes,
    write_cdes_excel,
)
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

    # Set output directory
    args.output_dir = (
        args.output_dir
        if args.output_dir is not None
        else Path(args.cdes_json_file).parent
    )

    # Set path of log file
    args.log_file = (
        args.log_file
        if args.log_file is not None
        else (Path(args.output_dir) / "cdes_update.log").absolute()
    )
    # Set up logging with log file
    setup_logging(args.log_file)

    # Log script arguments
    logging.info(f"Starting script with arguments: {args}")

    # Load the CDEs
    cdes_data = load_cdes_json(args.cdes_json_file)
    cdes_wb = load_cdes_excel(args.cdes_excel_file)

    # Replace "-" and "_" characters by white space
    if args.command == "remove_dashes_and_underscores":
        (cdes_data, cdes_wb) = recursive_replace_dashes_and_underscores(
            cdes_data, cdes_wb
        )

    # Generate output file names for json and excel files
    out_cdes_json_fname = generate_output_path(
        args.cdes_json_file,
        output_dir=args.output_dir,
        output_suffix=args.output_suffix,
    )
    out_cdes_excel_fname = generate_output_path(
        args.cdes_excel_file,
        output_dir=args.output_dir,
        output_suffix=args.output_suffix,
    )
    # Write edited CDEs to json and excel files
    write_cdes(
        cdes_data,
        cdes_wb,
        out_cdes_json_fname,
        out_cdes_excel_fname,
        out_json_indent=args.output_json_indent,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
