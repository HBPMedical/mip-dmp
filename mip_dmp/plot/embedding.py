import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mip_dmp.process.embedding import generate_embeddings, reduce_embeddings_dimension

# Define colors used to plot the column and CDE code embeddings
COLORS = ["#0072B2", "#4fa08b"]  # '#009E73'

# Set seaborn style
sns.set_style("darkgrid")
sns.set(
    rc={
        "axes.facecolor": "#222222",
        "figure.facecolor": "#222222",
        "text.color": "white",
        "axes.edgecolor": "white",
        "patch.edgecolor": "#222222",
        "xtick.color": "white",
        "ytick.color": "white",
        "axes.labelcolor": "white",
    }
)


def scatterplot_embeddings(
    fig: plt.Figure,
    inputDataset: pd.DataFrame,
    targetCDEs: pd.DataFrame,
    embedding_method: str = "chars2vec",
    dim_reduction_method: str = "tsne",
):
    """Plot word embedding.

    Parameters
    ----------
    fig: plt.Figure
        Matplotlib figure to plot

    inputDataset : pd.DataFrame
        Input dataset.

    targetCDEs : pd.DataFrame
        Target CDEs.

    embedding_method : str
        Embedding method. Can be "chars2vec" or "glove".
        Default: "chars2vec".

    dim_reduction_method : str
        Dimensionality reduction method. Can be "tsne" or "pca".

    Returns
    -------
    fig : plt.figure
        Figure.
    """
    # Extract list of columns and CDE codes
    columns = inputDataset.columns
    cde_codes = targetCDEs["code"].unique()
    # Print info about method's inputs
    print(
        f"> Generating embeddings for {len(columns)} columns and {len(cde_codes)} CDE codes..."
    )
    print(f"  - Embedding method: {embedding_method}")
    # Generate embeddings
    column_embeddings = generate_embeddings(columns, embedding_method)
    cde_embeddings = generate_embeddings(cde_codes, embedding_method)
    # Reduce embeddings dimension to 3 components via t-SNE or PCA for visualization
    x_column, y_column, z_column = reduce_embeddings_dimension(
        column_embeddings, reduce_method=dim_reduction_method
    )
    x_cde, y_cde, z_cde = reduce_embeddings_dimension(
        cde_embeddings, reduce_method=dim_reduction_method
    )
    # Format data as pandas dataframe for plotting
    df = pd.DataFrame(
        {
            "x": list(x_column) + list(x_cde),
            "y": list(y_column) + list(y_cde),
            "z": list(z_column) + list(z_cde),
            "label": list(columns) + list(cde_codes),
            "type": ["column"] * len(x_column) + ["cde"] * len(x_column),
        }
    )
    print(df)
    # Create a scatter plot with different colors for each group
    ax = fig.add_subplot(111, projection="3d")
    for t, color in zip(df["type"].unique(), COLORS):
        ax.scatter(
            df.loc[df["type"] == t, "x"],
            df.loc[df["type"] == t, "y"],
            df.loc[df["type"] == t, "z"],
            color=color,
            label=t,
            picker=True,
        )
    # Set labels and show legend
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()

    # Define a function to handle PickEvent-type events on the scatterplot
    def pick_event_method(event):
        """Define a function to pick event on the scatter plot (artist)."""

        def handle_annotations(artist, indices):
            """Add text annotations to closest point of the cursor when the mouse button was pressed."""
            texts = []
            for ind in indices:
                points_x, points_y, points_z = artist._offsets3d
                (x, y, z) = (
                    points_x[ind].__float__(),
                    points_y[ind].__float__(),
                    points_z[ind].__float__(),
                )
                # x, y, z = get_xyz_mouse_click(event, ax)
                # Find the closest point in the dataframe
                idx = (
                    (df["x"] - x) ** 2 + (df["y"] - y) ** 2 + (df["z"] - z) ** 2
                ).idxmin()
                # Get the value of src for the selected point
                val = df.loc[idx, "type"]
                # create the annotation text based on the value of src
                text = f"{df.loc[idx, 'label']}"
                print(f"Mouse click at ({x}, {y}, {z}) for label {text}")
                # Add jitter for overlapping points if needed
                # (x, y, z) = (x, y, z)
                # Add the annotation to the plot with the selected color based on type
                if val == "column":
                    ax.text(
                        x,
                        y,
                        z,
                        text,
                        fontsize=10,
                        color=COLORS[0],
                        backgroundcolor="#2222",
                        fontweight="bold",
                    )
                elif val == "cde":
                    ax.text(
                        x,
                        y,
                        z,
                        text,
                        fontsize=10,
                        color=COLORS[1],
                        backgroundcolor="#2222",
                        fontweight="bold",
                    )
                texts.append(text)
            # remove previous annotations
            for annotation in ax.texts:
                if annotation.get_text() not in texts:
                    annotation.remove()

        # Get the coordinates of the point clicked
        handle_annotations(event.artist, event.ind)
        # redraw the canvas
        fig.canvas.draw()

    # Connect the pick_event_method function to the figure
    fig.canvas.mpl_connect("pick_event", pick_event_method)
    # Return the figure
    return fig
