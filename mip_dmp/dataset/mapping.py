"""Module that provides functions to support the mapping of datasets to a specific CDEs metadata schema."""

from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
from scipy import spatial
import gensim.downloader as api
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # noqa
import chars2vec


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


# Define the function to find fuzzy matches
def fuzzy_match(x, choices):
    """Find the fuzzy matches for the given string.

    Parameters
    ----------
    x : str
        String for which the fuzzy matches are found.

    choices : list
        List of strings to be matched.

    Returns
    -------
    list
        List of fuzzy matches.
    """
    return [(m, fuzz.ratio(x, m), -fuzz.ratio(x, m)) for m in choices]


# Define the function to find the embedding vector representation for the text
def glove_embedding(text, glove_model):
    """Find the Glove embedding for the text.

    Parameters
    ----------
    text : str
        Text to be embedded.

    glove_model : str
        Glove model to be used, loaded by the gensim library.

    Returns
    -------
    numpy.ndarray
        Glove embedding for the text.
    """

    def preprocess_text(text):
        """Preprocess the text.

        Parameters
        ----------
        text : str
            Text to be preprocessed.

        Returns
        -------
        str
            Preprocessed text.
        """
        # Lowercase the text.
        text = text.lower()
        # Tokenize the text.
        text = [s for s in text if s != "" and s != "_"]  # Make a list of characters.
        return text

    # Preprocess the text.
    text = preprocess_text(text)
    # Find the Glove embedding for the text.
    embedding = np.sum(np.array([glove_model[i] for i in text]), axis=0)
    return embedding


def chars2vec_embedding(text, chars2vec_model):
    """Find the chars2vec embedding for the text.

    Parameters
    ----------
    text : str
        Text to be embedded.

    chars2vec_model : str
        chars2vec model to be used, loaded by the gensim library.

    Returns
    -------
    numpy.ndarray
        chars2vec embedding for the text.
    """
    # Find the chars2vec embedding for the text.
    # The chars2vec model expects a list of strings as input.
    # The output is a list of embeddings, so we take the first element.
    embedding = chars2vec_model.vectorize_words([text])[0]
    return embedding


def embedding_similarity(x_embedding, y_embedding):
    """Find the matches based on chars2vec embeddings and cosine similarity.

    Parameters
    ----------
    x_embedding : str
        String to compare against.

    y_embedding : str
        String to compare.

    chars2vec_model : str
        chars2vec model to be used, loaded by the gensim library.

    Returns
    -------
    float
        Cosine similarity between the two chars2vec embeddings of the strings.
    """
    return spatial.distance.cosine(x_embedding, y_embedding)


def initialize_mapping_table(
    dataset,
    schema,
    nb_kept_matches=10,
    matching_method="fuzzy",
    glove_model_name="glove-wiki-gigaword-50",
):
    """Initialize the mapping table.

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
        glove_model = api.load(glove_model_name)
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
        c2v_model = chars2vec.load_model("eng_50")
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
