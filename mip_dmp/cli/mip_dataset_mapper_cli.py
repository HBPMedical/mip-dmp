# Copyright 2023 The HIP team, University Hospital of Lausanne (CHUV), Switzerland & Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Standalone script which runs the MIP Dataset Mapper from the terminal."""

import sys
from pathlib import Path

# import logging
from mip_dmp.process.mapping import map_dataset

from mip_dmp.io import (
    load_csv,
    load_excel,
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
    # Set cdes file path
    args.cdes_file = Path(args.cdes_file).absolute()
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
    cde_codes = load_excel(args.cdes_file)["code"].unique().tolist()
    # Map the input dataset to the target CDEs
    output_dataset = map_dataset(source_dataset, mappings, cde_codes)
    # Save the output dataset
    output_dataset.to_csv(
        args.target_dataset,
        index=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
