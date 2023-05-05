"""Module that provides functions to support the mapping of datasets to a specific CDEs metadata schema."""

# External imports
import os
import numpy as np
import pandas as pd

# Disable Tensorflow warnings, other options are:
# - 0 (default): all messages are logged (default behavior)
# - 1: INFO messages are not printed
# - 2: INFO and WARNING messages are not printed
# - 3: INFO, WARNING, and ERROR messages are not printed
# Note: this has to be done before importing tensorflow
# that is done when importing chars2vec in mip_dmp/io.py
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # noqa

# Constants
MAPPING_TABLE_COLUMNS = {
    "dataset_column": [],
    "cde_code": [],
    "cde_type": [],
    "transform_type": [],
    "transform": [],
}


def map_dataset(dataset, mappings):
    """Map the dataset to the schema.

    Parameters
    ----------
    dataset : pandas.DataFrame
        Dataset to be mapped.

    mappings : dict
        Mappings of the dataset columns to the schema columns.

    Returns
    -------
    pandas.DataFrame
        Mapped dataset.
    """
    # create a list to hold the mapped columns
    mapped_columns = []

    # Map and apply transformation to each dataset column described in the
    # mapping JSON file.
    for mapping in mappings:
        # Extract the mapping information of the column.
        dataset_column = mapping["dataset_column"]
        cde_code = mapping["cde_code"]
        cde_type = mapping["cde_type"]
        transform_type = mapping["transform_type"]
        transform = mapping["transform"]
        # Copy the dataset column to the mapped dataset for which the column name
        # is the CDE code.
        # map the input data to the CDE code and append to the list of mapped columns

        # Apply the transformation to the mapped dataset column.
        mapped_columns.append(
            transform_dataset_column(
                dataset[dataset_column].rename(cde_code),
                cde_code,
                cde_type,
                transform_type,
                transform,
            )
        )
    mapped_dataset = pd.concat(mapped_columns, axis=1)
    # Return the mapped dataset.
    print(mapped_dataset)
    return mapped_dataset


def transform_dataset_column(
    dataset_column, cde_code, cde_type, transform_type, transform
):
    """Transform the dataset column.

    Parameters
    ----------
    dataset_column : pandas.DataFrame
        Dataset column to be transformed.

    cde_code : str
        CDE code of the dataset column.

    cde_type : str
        CDE type of the dataset column. Can be "binomial", "multinomial", "integer" or "real".

    transform_type : str
        Type of transformation to be applied to the dataset column.
        Can be "map" or "scale".

    transform : str
        Transformation to be applied to the dataset column.
        Can be a JSON string for the "map" transformation type or a scaling factor.

    Returns
    -------
    dataset_column: pandas.DataFrame
        The transformed dataset column.
    """
    # Apply the transformation only if not NaN.
    if transform_type == "map" and transform != "nan":
        dataset_column = apply_transform_map(dataset_column, transform)
    elif transform_type == "scale" and transform != "nan":
        # Apply the scaling factor.
        scaling_factor = float(transform)
        dataset_column = apply_transform_scale(
            dataset_column, cde_code, cde_type, scaling_factor
        )
    else:
        print(f"WARNING: No transformation applied for output column {cde_code}.")
    return dataset_column


def apply_transform_map(dataset_column, transform):
    """Apply the transform map for binomial and multinominal variables.

    Parameters
    ----------
    dataset_column : pandas.DataFrame
        Dataset column to be transformed.

    transform : str
        Transformation to be applied to the dataset column.
        Can be a JSON string for the "map" transformation type or a scaling factor.

    Returns
    -------
    dataset_column: pandas.DataFrame
        The transformed dataset column."""
    # Parse the mapping values from the JSON string
    mapping_values = eval(transform)
    # Map the values.
    for mapping_value_item in mapping_values.items():
        old_value = mapping_value_item[0]
        new_value = mapping_value_item[1]
        dataset_column.iloc[dataset_column == old_value] = new_value
    return dataset_column


def apply_transform_scale(dataset_column, cde_code, cde_type, scaling_factor):
    """Apply the transform scale for real and integer variables.

    Parameters
    ----------
    dataset_column : pandas.DataFrame
        Dataset column to be transformed.

    cde_code : str
        CDE code of the dataset column.

    cde_type : str
        CDE type of the dataset column. Can be "binomial", "multinomial", "integer" or "real".

    scaling_factor : float
        Scaling factor to be applied to the dataset column.

    Returns
    -------
    dataset_column: pandas.DataFrame
        The transformed dataset column.
    """
    # Check if the column contains any NaN values. If so, the scaling is
    # not applied. Otherwise, the scaling is applied.
    if not dataset_column.isnull().values.any():
        # Cast the column to the correct type and apply the scaling factor.
        if cde_type == "integer":
            dataset_column = dataset_column.astype(int) * int(scaling_factor)
        elif cde_type == "real":
            dataset_column = dataset_column.astype(float) * scaling_factor
    else:
        # Cast and scale only the non-NaN values.
        if cde_type == "integer":
            dataset_column_list = [
                np.nan if pd.isnull(x) else int(float(x)) * int(scaling_factor)
                for x in dataset_column
            ]
        elif cde_type == "real":
            dataset_column_list = [
                np.nan if pd.isnull(x) else float(x) * scaling_factor
                for x in dataset_column
            ]
        dataset_column = pd.DataFrame(dataset_column_list, columns=[cde_code])
    return dataset_column
