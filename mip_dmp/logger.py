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

"""Module to setup logging for the MIP Dataset Mapper."""

import logging


def setup_logging(log_file):
    """Set up logging and log file.

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
        filemode="w",
    )
