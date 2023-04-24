"""Standalone script which runs the MIP Dataset Mapper from the terminal."""

import sys
from pathlib import Path

# import logging
from mip_dmp.dataset.mapping import map_dataset

from mip_dmp.io import (
    load_csv,
    # load_excel,
    load_json,
)
from mip_dmp.parser import create_parser

# from mip_dmp.logger import setup_logging


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
    # Set source dataset file path
    args.source_dataset = Path(args.source_dataset).absolute()
    # Set mapping file path
    args.mapping_file = Path(args.mapping_file).absolute()
    # Set target dataset file path
    args.target_dataset = Path(args.target_dataset).absolute()
    # Set path of log file
    # args.log_file = (
    #     args.log_file
    #     if args.log_file is not None
    #     else (Path(args.output_dir) / "cdes_update.log").absolute()
    # )
    # Set up logging with log file
    # setup_logging(args.log_file)
    # Log script arguments
    # logging.information(f"Starting script with arguments: {args}")
    print(f"Starting script with arguments: {args}")
    # Load the files
    print("Loading the files...")
    source_dataset = load_csv(args.source_dataset)
    mappings = load_json(args.mapping_file)
    # Map the input dataset to the target CDEs
    output_dataset = map_dataset(source_dataset, mappings)
    # Save the output dataset
    output_dataset.to_csv(
        args.target_dataset,
        index=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
