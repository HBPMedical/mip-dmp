"""Module for logging.""" ""

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
