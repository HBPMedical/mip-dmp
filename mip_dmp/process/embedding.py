"""Functions that provides function to handle word embeddings and operations on them."""

# External imports
import numpy as np
from scipy import spatial
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

# Internal imports
from mip_dmp.io import load_glove_model, load_c2v_model


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


def generate_embeddings(words: list, embedding_method: str = "chars2vec"):
    """Generate embeddings for a list of words.

    Parameters
    ----------
    words : list
        List of words to generate embeddings for.

    embedding_method : str
        Embedding method to be used, either "chars2vec" or "glove".

    Returns
    -------
    list
        List of embeddings for the words.
    """
    print(f"> Generating embeddings for {len(words)} words...")
    if embedding_method == "chars2vec":
        c2v_model = load_c2v_model()
        embeddings = [chars2vec_embedding(word, c2v_model) for word in words]
    elif embedding_method == "glove":
        glove_model = load_glove_model()
        embeddings = [glove_embedding(word, glove_model) for word in words]
    else:
        embeddings = None
    return embeddings


def find_n_closest_embeddings(
    word_embedding: np.array, embeddings: list, embedding_words: list, n: int = 5
):
    """Find the n closest embeddings to the given embedding.

    Parameters
    ----------
    word_embedding : numpy.ndarray
        Embedding to find the n closest embeddings to.

    embeddings : list
        List of embeddings to find the closest embeddings to the given embedding in.

    embedding_words : list
        List of words corresponding to the embeddings that will be resorted and reduced accordingly.

    n : int
        Number of closest embeddings to find.

    Returns
    -------
    dict
        Dictionary containing the n closest embeddings, their distances to the given embedding,
        and the words corresponding to the embeddings in the form::

            {
                "distances": [float],
                "embeddings": [numpy.ndarray],
                "embedding_words": [str]
            }
    """
    distances = np.array(
        [spatial.distance.cosine(word_embedding, embedding) for embedding in embeddings]
    ).astype(np.float32)
    sorted_indices = np.argsort(distances)
    return dict(
        {
            "distances": [distances[i] for i in sorted_indices[0:n]],
            "embeddings": [embeddings[i] for i in sorted_indices[0:n]],
            "embedding_words": [embedding_words[i] for i in sorted_indices[0:n]],
        }
    )


def reduce_embeddings_dimension(
    embeddings: list, reduce_method: str = "tsne", n_components: int = 3
):
    """Reduce the dimension of the embeddings, mainly for visualization purposes.

    Parameters
    ----------
    embeddings : list
        List of embeddings to reduce the dimension of.

    reduce_method : str
        Method to use to reduce the dimension, either "tsne" or "pca".

    n_components : int
        Number of components to reduce the dimension to.

    Returns
    -------
    list
        List of reduced embeddings.
    """
    print(
        f"> Reducing embeddings dimensionality to {n_components} using {reduce_method}..."
    )
    if reduce_method == "tsne":
        tsne_model = TSNE(
            perplexity=40,
            n_components=n_components,
            init="pca",
            n_iter=2500,
            random_state=42,
        )
        reduction_values = tsne_model.fit_transform(np.array(embeddings))
    elif reduce_method == "pca":
        pca_model = PCA(n_components=n_components, random_state=42)
        reduction_values = pca_model.fit_transform(np.array(embeddings))
    else:
        print(f"ERROR: Invalid reduction method ({reduce_method})!")
        reduction_values = None
    return (
        reduction_values[:, 0],
        reduction_values[:, 1],
        reduction_values[:, 2],
    )
