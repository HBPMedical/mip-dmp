"""Module that provides functions to support the matching of dataset columns to CDEs."""

# External imports
import pandas as pd
from fuzzywuzzy import fuzz

# Internal imports
from mip_dmp.io import load_glove_model, load_c2v_model
from mip_dmp.process.mapping import MAPPING_TABLE_COLUMNS
from mip_dmp.process.embedding import (
    glove_embedding,
    chars2vec_embedding,
    embedding_similarity,
)


def match_columns_to_cdes(
    dataset,
    schema,
    nb_kept_matches=10,
    matching_method="fuzzy",
    glove_model_name="glove-wiki-gigaword-50",
):
    """Initialize the mapping table by matching the dataset columns with the CDE codes.

    Different matching methods can be used:
    - "fuzzy": Fuzzy matching using the Levenshtein distance. (https://github.com/seatgeek/thefuzz)
    - "glove": Embedding matching using Glove embeddings at the character level. (https://nlp.stanford.edu/projects/glove/)
    - "chars2vec": Embedding matching using Chars2Vec embeddings. (https://github.com/IntuitionEngineeringTeam/chars2vec)

    Parameters
    ----------
    dataset : pandas.DataFrame
        Dataset to be mapped.

    schema : pandas.DataFrame
        Schema to which the dataset is mapped.

    nb_kept_matches : int
        Number of matches to keep for each dataset column.

    matching_method : str
        Method to be used for matching the dataset columns with the CDE codes.
        Can be "fuzzy", "glove" or "chars2vec".

    glove_model_name : str
        Name of the Glove model to be used for matching the dataset columns
        with the CDE codes.

    Returns
    -------
    pandas.DataFrame
        Mapping table represented as a Pandas DataFrame.

    matched_cde_codes : dict
        Dictionary with tuple of the first 10 matched CDE codes with
        corresponding fuzzy ratio / cosine similarity (value) for each dataset column (key).
    """
    # Create the mapping table.
    mapping_table = pd.DataFrame(MAPPING_TABLE_COLUMNS)

    # Add the dataset columns.
    mapping_table["dataset_column"] = dataset.columns

    # Initialize a dictionary to store the results of the
    # first 10 matched CDE codes for each dataset column.
    matched_cde_codes = {}

    if matching_method == "fuzzy":
        print(f"> Perform fuzzy matching with {nb_kept_matches} matches per column.")
        # Function to find the fuzzy matches for each dataset column.
        matches = mapping_table["dataset_column"].apply(
            lambda dataset_column: str(
                sorted(
                    schema["code"],
                    key=lambda cde_code: fuzz.ratio(dataset_column, cde_code),
                    reverse=True,
                )[
                    0:nb_kept_matches
                ]  # Select the nb_kept_matches first matched CDE codes.
            )
        )
    elif matching_method == "glove":
        print(
            f"> Perform Glove embedding matching with {nb_kept_matches} matches per column."
        )
        # Function to find the matches based on Glove embeddings and cosine similarity.
        glove_model = load_glove_model(glove_model_name)
        matches = mapping_table["dataset_column"].apply(
            lambda dataset_column: str(
                sorted(
                    schema["code"],
                    key=lambda cde_code: embedding_similarity(
                        glove_embedding(dataset_column, glove_model),
                        glove_embedding(cde_code, glove_model),
                    ),
                )[
                    0:nb_kept_matches
                ]  # Select the nb_kept_matches first matched CDE codes.
            )
        )
    elif matching_method == "chars2vec":
        print(
            f"> Perform chars2vec embedding matching with {nb_kept_matches} matches per column."
        )
        # Function to find the matches based on chars2vec embeddings and cosine similarity.
        c2v_model = load_c2v_model("eng_50")
        matches = mapping_table["dataset_column"].apply(
            lambda dataset_column: str(
                sorted(
                    schema["code"],
                    key=lambda cde_code: embedding_similarity(
                        chars2vec_embedding(dataset_column, c2v_model),
                        chars2vec_embedding(cde_code, c2v_model),
                    ),
                )[
                    0:nb_kept_matches
                ]  # Select the nb_kept_matches first matched CDE codes.
            )
        )
    matches = matches.apply(lambda x: eval(x))

    # Store the first nb_fuzy_matches matched CDE codes in the dictionary.
    for i, dataset_column in enumerate(dataset.columns):
        if matching_method == "fuzzy":
            matched_cde_codes[dataset_column] = (
                matches[i][:nb_kept_matches],
                [
                    fuzz.ratio(dataset_column, match)
                    for match in matches[i][:nb_kept_matches]
                ],
            )
        elif matching_method == "glove":
            matched_cde_codes[dataset_column] = (
                matches[i][:nb_kept_matches],
                [
                    embedding_similarity(
                        glove_embedding(dataset_column, glove_model),
                        glove_embedding(match, glove_model),
                    )
                    for match in matches[i][:nb_kept_matches]
                ],
            )
        elif matching_method == "chars2vec":
            matched_cde_codes[dataset_column] = (
                matches[i][:nb_kept_matches],
                [
                    embedding_similarity(
                        chars2vec_embedding(dataset_column, c2v_model),
                        chars2vec_embedding(match, c2v_model),
                    )
                    for match in matches[i][:nb_kept_matches]
                ],
            )
    # Add the first matched CDE code for each dataset_column.
    mapping_table["cde_code"] = [match[0] for match in matches]

    # Add the CDE type corresponding to the CDE code proposed by fuzzy matching.
    mapping_table["cde_type"] = [
        schema[schema["code"] == cde_code]["type"].iloc[0]
        for cde_code in mapping_table["cde_code"]
    ]

    # Add the transform type based on the CDE type (integer, real, binominal, multinominal).
    mapping_table["transform_type"] = [
        "scale" if cde_type in ["integer", "real"] else "map"
        for cde_type in mapping_table["cde_type"]
    ]

    # Add the transform.
    mapping_table["transform"] = [
        make_initial_transform(dataset, schema, dataset_column, cde_code)
        for (dataset_column, cde_code) in zip(
            mapping_table["dataset_column"], mapping_table["cde_code"]
        )
    ]

    return (mapping_table, matched_cde_codes)


def make_initial_transform(dataset, schema, dataset_column, cde_code):
    """Make the initial transform.

    Parameters
    ----------
    dataset : pandas.DataFrame
        Dataset to be mapped.

    schema : pandas.DataFrame
        Schema to which the dataset is mapped.

    dataset_column : str
        Dataset column.

    cde_code : str
        CDE code.

    Returns
    -------
    dict
        Initial transform.
    """
    # Get the CDE type.
    cde_type = schema[schema["code"] == cde_code]["type"].iloc[0]

    # Make the initial transform.
    if cde_type in ["integer", "real"]:
        return "1.0"
    elif cde_type in ["binominal", "multinominal"]:
        # Extract the CDE code values from the corresponding cell of
        # the "values" column of the schema.
        cde_code_values_str = (
            f'[{schema[schema["code"] == cde_code]["values"].iloc[0]}]'
        )
        # Replace problematic characters.
        cde_code_values_str = cde_code_values_str.replace("“", '"')
        cde_code_values_str = cde_code_values_str.replace("”", '"')
        # Replace curly brackets to convert the string to a list of tuples.
        cde_code_values_str = cde_code_values_str.replace("{", "(")
        cde_code_values_str = cde_code_values_str.replace("}", ")")
        # Convert the string to a list of tuples.
        cde_code_values = eval(cde_code_values_str)
        # Extract the values from the list of tuples as a list of strings.
        cde_code_values = [
            f"{str(cde_code_value[0])}" for cde_code_value in cde_code_values
        ]
        # Get the unique values of the dataset column and make sure they are strings.
        dataset_column_values = [
            f"{str(dataset_column_value)}"
            for dataset_column_value in dataset[dataset_column].unique()
        ]
        # Define the initial transform.
        initial_transform = generate_initial_transform(
            dataset_column_values,
            cde_code_values,
            dataset_column,
        )
        return initial_transform
    else:
        raise ValueError(f"Unknown CDE type: {cde_type}")


def generate_initial_transform(dataset_column_values, cde_code_values, dataset_column):
    """Generate the initial transform.

    Parameters
    ----------
    dataset_column_values : list of str
        Dataset column values.

    cde_code_values : list of str
        CDE code values.

    dataset_column : str
        Dataset column.

    Returns
    -------
    initial_transform : str
        Initial transform.
    """
    # Handle the case where the dataset column values are all NaN.
    if (
        len(dataset_column_values) == 1
        and dataset_column_values[0] == "nan"
        and ("nan" not in cde_code_values)
    ):
        print(
            f"WARNING: The dataset column {dataset_column} present only one NaN value."
        )
        return "nan"
    elif "nan" in dataset_column_values:
        nb_nan_values = dataset_column_values.count("nan")
        if nb_nan_values == len(dataset_column_values):
            print(
                f"WARNING: The dataset column {dataset_column} present only NaN values."
            )
            return "nan"
    # Handle the case where we have the same number of dataset column values
    # and CDE code values.
    if len(dataset_column_values) == len(cde_code_values):
        # Fuzzy match dataset column values to the CDE code values
        cde_code_values = [
            sorted(
                cde_code_values,
                key=lambda cde_code_value, dataset_column_value=dataset_column_value: fuzz.ratio(
                    dataset_column_value, cde_code_value
                ),
                reverse=True,
            )[0]
            for dataset_column_value in dataset_column_values
        ]
        return str(
            {
                f"{dataset_column_value}": f"{cde_code_value}"
                for dataset_column_value, cde_code_value in zip(
                    dataset_column_values, cde_code_values
                )
            }
        )
    # Handle the case where we have less dataset column values than CDE code values.
    # In this case, we map the dataset column values to the first CDE code values.
    # This is not ideal, but it is the best we can do. The user can fix this later.
    elif len(dataset_column_values) < len(cde_code_values):
        return str(
            {
                f"{dataset_column_value}": f"{cde_code_values[index]}"
                for index, dataset_column_value in enumerate(dataset_column_values)
                if (dataset_column_value == "nan" and cde_code_values[index] == "nan")
                or (dataset_column_value != "nan" and cde_code_values[index] != "nan")
            }
        )
    # Handle the case where we have more dataset column values than CDE code values.
    # In this case, we map the dataset column values to NaN and MUST BE FIXED by the user.
    elif len(dataset_column_values) > len(cde_code_values):
        return str(
            {
                f"{dataset_column_value}": "nan"
                for dataset_column_value in dataset_column_values
            }
        )
