import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# import plotly as py
# import plotly.graph_objs as go

from mip_dmp.io import load_glove_model, load_c2v_model
from mip_dmp.dataset.mapping import glove_embedding, chars2vec_embedding


def embedding_vizualization_figure(
    inputDataset: pd.DataFrame,
    targetCDEs: pd.DataFrame,
    embedding_method: str = "chars2vec",
):
    """Plot word embedding.

    Parameters
    ----------
    inputDataset : pd.DataFrame
        Input dataset.

    targetCDEs : pd.DataFrame
        Target CDEs.

    embedding_method : str
        Embedding method. Can be "chars2vec" or "glove".
        Default: "chars2vec".

    Returns
    -------
    fig : plt.figure
        Figure.
    """
    columns = inputDataset.columns
    print(f"Columns: {columns}")
    cde_codes = targetCDEs["code"].unique()
    print(f"CDE codes: {cde_codes}")
    print(f"Embedding method: {embedding_method}")

    if embedding_method == "chars2vec":
        c2v_model = load_c2v_model()
        column_embeddings = [
            chars2vec_embedding(column, c2v_model) for column in columns
        ]
        cde_embeddings = [
            chars2vec_embedding(cde_code, c2v_model) for cde_code in cde_codes
        ]
    elif embedding_method == "glove":
        glove_model = load_glove_model()
        column_embeddings = [glove_embedding(column, glove_model) for column in columns]
        cde_embeddings = [
            glove_embedding(cde_code, glove_model) for cde_code in cde_codes
        ]
    else:
        return None

    tsne_model = TSNE(
        perplexity=40, n_components=3, init="pca", n_iter=2500, random_state=23
    )
    column_tsne_values = tsne_model.fit_transform(np.array(column_embeddings))
    cde_tsne_values = tsne_model.fit_transform(np.array(cde_embeddings))

    x_column = []
    y_column = []
    z_column = []
    for value in column_tsne_values:
        x_column.append(value[0])
        y_column.append(value[1])
        z_column.append(value[2])

    x_cde = []
    y_cde = []
    z_cde = []
    for value in cde_tsne_values:
        x_cde.append(value[0])
        y_cde.append(value[1])
        z_cde.append(value[2])

    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(111, projection="3d")

    for i in range(len(x_column)):
        ax.scatter(x_column[i], y_column[i], z_column[i], marker="o", color="green")
        ax.text(
            x_column[i],
            y_column[i],
            z_column[i],
            "%s" % (columns[i]),
            size=20,
            zorder=1,
            color="green",
        )

    for i in range(len(x_cde)):
        ax.scatter(x_cde[i], y_cde[i], z_cde[i], marker="^", color="k")
        ax.text(
            x_cde[i],
            y_cde[i],
            z_cde[i],
            "%s" % (cde_codes[i]),
            size=20,
            zorder=1,
            color="k",
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    return fig
