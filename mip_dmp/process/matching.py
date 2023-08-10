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

"""Module that provides functions to support the matching of dataset columns to CDEs."""

# External imports
import ast
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

# Internal imports
from mip_dmp.process.mapping import MAPPING_TABLE_COLUMNS
from mip_dmp.process.embedding import (
    generate_embeddings,
    find_n_closest_embeddings,
)
from mip_dmp.process.utils import is_number


def match_columns_to_cdes(
    dataset,
    schema,
    nb_kept_matches=10,
    matching_method="fuzzy",
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

    Returns
    -------
    pandas.DataFrame
        Mapping table represented as a Pandas DataFrame.

    matched_cde_codes : dict
        Dictionary of dictionaries storing the first 10 matched CDE codes with
        corresponding fuzzy ratio / cosine similarity (value) / and embedding vector
        for each dataset column (key). It has the form::

            {
                "dataset_column_1": {
                    "words": ["cde_code_1", "cde_code_2", ...],
                    "distances": [0.9, 0.8, ...],
                    "embeddings": [None, None, ...]
                },
                "dataset_column_2": {
                    "words": ["cde_code_1", "cde_code_2", ...],
                    "distances": [0.9, 0.8, ...],
                    "embeddings": [None, None, ...]
                },
                ...
            }

    dataset_column_embeddings : list
        List of embedding vectors for the dataset columns.

    schema_code_embeddings : list
        List of embedding vectors for the CDE codes.
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
        dataset_column_embeddings, schema_code_embeddings = (
            None,
            None,
        )  # Not used for fuzzy matching.
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
        # Store the first nb_fuzzy_matches matched CDE codes in the dictionary.
        for i, dataset_column in enumerate(dataset.columns):
            words = ast.literal_eval(matches.to_list()[i])
            matched_cde_codes[dataset_column] = {
                "words": words,
                "distances": [
                    (1 - 0.01 * fuzz.ratio(dataset_column, match)) for match in words
                ],
                "embeddings": [None] * nb_kept_matches,
            }
    elif matching_method == "chars2vec" or matching_method == "glove":
        print(
            f"> Perform  {matching_method} embedding matching with {nb_kept_matches} matches per column."
        )
        dataset_column_embeddings, schema_code_embeddings = (
            generate_embeddings(mapping_table["dataset_column"], matching_method),
            generate_embeddings(schema["code"], matching_method),
        )
        print(f"> Find {nb_kept_matches} closest embeddings for each dataset column...")
        n_closest_matches = [
            find_n_closest_embeddings(
                dataset_column_embedding,
                schema_code_embeddings,
                schema["code"],
                nb_kept_matches,
            )
            for dataset_column_embedding in dataset_column_embeddings
        ]
        matched_cde_codes = {
            dataset_column: {
                "words": n_closest_matches[i]["embedding_words"],
                "distances": n_closest_matches[i]["distances"],
                "embeddings": n_closest_matches[i]["embeddings"],
            }
            for i, dataset_column in enumerate(mapping_table["dataset_column"])
        }
    # Add the first matched CDE code for each dataset_column.
    mapping_table["cde_code"] = [
        matched_cde_codes[k]["words"][0] for k in matched_cde_codes.keys()
    ]
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
    return (
        mapping_table,
        matched_cde_codes,
        dataset_column_embeddings,
        schema_code_embeddings,
    )


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
    elif cde_type in ["binominal", "multinominal", "nominal"]:
        # Extract the string CDE code encoded / text values from the corresponding cell of
        # the "values" column of the schema, and format it as a dictionary of the form:
        # {encoded_value_1: text_value_1, encoded_value_2: text_value_2, ...}
        cde_code_values_str = (
            f'[{schema[schema["code"] == cde_code]["values"].iloc[0]}]'
        )
        # Replace problematic characters.
        cde_code_values_str = cde_code_values_str.replace("“", '"')
        cde_code_values_str = cde_code_values_str.replace("”", '"')
        # Remove surrounding brackets
        cde_code_values_str = cde_code_values_str.replace("[", "")
        cde_code_values_str = cde_code_values_str.replace("]", "")
        # Convert the string to a dictionary.
        cde_code_values_dict = eval(cde_code_values_str)
        # Get the unique values of the dataset column and make sure they are strings.
        dataset_column_values = [
            f"{str(dataset_column_value)}"
            for dataset_column_value in dataset[dataset_column].unique()
        ]
        # Extract the CDE code encoded / text values from the dictionary
        # previously created.
        if any(is_number(s) for s in dataset_column_values):
            # If the dataset column values contain numbers,
            # it means we relabel the encoded integer values
            # with the new corresponding encoded values of the schema.
            cde_code_values = [
                f"{str(key)}"
                for key in cde_code_values_dict
            ]
        else:
            # If the dataset column values do not contain numbers,
            # it means we relabel the text values with the new
            # corresponding text values of the schema.
            cde_code_values = [
                f"{str(cde_code_values_dict[key])}"
                for key in cde_code_values_dict
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
        print(f"WARNING: The dataset column {dataset_column} has only one NaN value.")
        return "nan"
    elif "nan" in dataset_column_values:
        nb_nan_values = dataset_column_values.count("nan")
        if nb_nan_values == len(dataset_column_values):
            print(f"WARNING: The dataset column {dataset_column} has only NaN values.")
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


def make_distance_vector(matchedCdeCodes, inputDatasetColumn):
    """Make the n closest match distance vector.

    Parameters
    ----------
    matchedCdeCodes : dict
        Dictionary of the matching results in the form::

            {
                "inputDatasetColumn1": {
                    "words": ["word1", "word2", ...],
                    "distances": [distance1, distance2, ...],
                    "embeddings": [embedding1, embedding2, ...]
                },
                "inputDatasetColumn2": {
                    "words": ["word1", "word2", ...],
                    "distances": [distance1, distance2, ...],
                    "embeddings": [embedding1, embedding2, ...]
                },
                ...
            }

    inputDatasetColumn : lstr
        Input dataset column name.

    Returns
    -------
    distanceVector : numpy.ndarray
        Similarity/distance vector.
    """
    # Get the matched CDE codes for the current input dataset column
    matches = matchedCdeCodes[inputDatasetColumn]
    # Initialize the similarity matrix
    similarityVector = np.zeros((1, len(matches["words"])))
    # Update the similarity matrix
    similarityVector[0, :] = matches["distances"]
    # Return the similarity matrix
    return similarityVector


def match_column_to_cdes(
    dataset_column,
    schema
):
    """Match a dataset column to CDEs using fuzzy matching.

    Parameters
    ----------
    dataset_column : str
        Dataset column.

    schema : pandas.DataFrame
        Schema to which the dataset is mapped.

    Returns
    -------
    list
        List of matched CDE codes ordered by decreasing fuzzy ratio.
    """
    # Function to find the fuzzy matches for each dataset column.
    matches = sorted(
        schema["code"],
        key=lambda cde_code: fuzz.ratio(dataset_column, cde_code),
        reverse=True,
    )
    return matches
