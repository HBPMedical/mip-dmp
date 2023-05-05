import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mip_dmp.process.embedding import generate_embeddings, reduce_embeddings_dimension

# Define colors used to plot the column and CDE code embeddings
# '#4fa08b' green / '#009E73' green / '#0072B2' blue / '#FFA500' orange
COLORS = ["#0072B2", "#FFA500"]
# Set seaborn style
sns.set_style("darkgrid")
sns.set(
    rc={
        "axes.facecolor": "#081512",
        "figure.facecolor": "#081512",
        "text.color": "white",
        "axes.edgecolor": "white",
        "patch.edgecolor": "#081512",
        "xtick.color": "white",
        "ytick.color": "white",
        "axes.labelcolor": "white",
        "grid.color": "#4fa08b",
        "axes3d.xaxis.panecolor": "#081512",
        "axes3d.yaxis.panecolor": "#081512",
        "axes3d.zaxis.panecolor": "#081512",
    }
)


def scatterplot_embeddings(
    fig: plt.Figure, embeddings: dict, matchedCdeCodes: dict, selectedColumnName: str
):
    """Plot the embeddings of the selected column name and CDE codes in a 3D scatter plot.

    fig: matplotlib.figure.Figure
        Figure to render the 3D scatter plot of the embeddings.

    embeddings: dict
        Dictionary of embeddings in the form::

            {
                "x": [5, ..., 2],
                "y": [0.5, ..., 0.2],
                "z": [0.5, ..., 0.2],
                "label": ["word1", ..., "wordN"],
                "type": ["cde", ..., "column"]
            }

        where `x`, `y` and `z` are the lists of the x, y and z coordinates of the embeddings,
        `label` is the list of the labels of the embeddings and `type` is the list of the
        types of the embeddings (can be "column" or "cde").

    matchedCdeCodes: dict
        Dictionary of the matched CDE codes in the form::

            {
                "input_dataset_column1": {
                    "words": ["cde_code1", "cde_code2", ...],
                    "embeddings": [embedding_vector1, embedding_vector2, ...]
                    "distances": [distance1, distance2, ...]
                },
                "input_dataset_column2": {
                    "words": ["cde_code1", "cde_code2", ...],
                    "embeddings": [embedding_vector1, embedding_vector2, ...]
                    "distances": [distance1, distance2, ...]
                },
                ...
            }

    selectedColumnName: str
        Name of the selected column.
    """
    print("> Generate scatterplot...")
    # Get the words for which their embeddings have been matched to column name
    selected_column_matches = matchedCdeCodes[selectedColumnName]["words"]
    # Generate filtered list of embeddings
    filtered_embeddings = {}
    for key in embeddings.keys():
        filtered_embeddings[key] = [
            embeddings[key][i]
            for i, t in enumerate(embeddings["type"])
            if t == "cde" and embeddings["label"][i] in selected_column_matches
        ] + [
            embeddings[key][i]
            for i, t in enumerate(embeddings["type"])
            if t == "column" and embeddings["label"][i] == selectedColumnName
        ]

    # Determine a scaled dynamic jittering for the scatter plot based on
    # the dynamic range of the data in the given dimension
    def rand_jitter(arr, scale=0.3):
        """Return random noise for jittering."""
        stdev = scale * (max(arr) - min(arr))
        return stdev

    stdev_x = rand_jitter(filtered_embeddings["x"])
    stdev_y = rand_jitter(filtered_embeddings["y"])
    stdev_z = rand_jitter(filtered_embeddings["z"])
    # Format data as pandas dataframe for plotting
    df = pd.DataFrame(
        {
            "x": filtered_embeddings["x"],
            "y": filtered_embeddings["y"],
            "z": filtered_embeddings["z"],
            "label": filtered_embeddings["label"],
            "type": filtered_embeddings["type"],
        }
    )
    # Create a scatter plot with different colors for each group
    ax = fig.add_subplot(111, projection="3d")
    artists = {}
    annotation_texts = {}
    for t, color in zip(df["type"].unique(), COLORS):
        artists[t] = ax.scatter(
            df.loc[df["type"] == t, "x"],
            df.loc[df["type"] == t, "y"],
            df.loc[df["type"] == t, "z"],
            color=color,
            label=t,
            picker=True,
            alpha=0.5,
            s=50,
        )
        annotation_texts[t] = []
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
            # Get the type of the artist that can be "cde" or "column"
            for k in artists.keys():
                if artist == artists[k]:
                    artist_type = k
            artist_df = df[df["type"] == artist_type]
            # For each index of the artist
            for ind in indices:
                # Get the coordinates of the mouse click
                points_x, points_y, points_z = artist._offsets3d
                (x, y, z) = (
                    points_x[ind].__float__(),
                    points_y[ind].__float__(),
                    points_z[ind].__float__(),
                )
                # Find the closest point in the dataframe
                idx = (
                    (artist_df["x"] - x) ** 2
                    + (artist_df["y"] - y) ** 2
                    + (artist_df["z"] - z) ** 2
                ).idxmin()
                # Get the corresponding label
                text = f"{artist_df.loc[idx, 'label']}"
                # print(
                #     f"Mouse click at ({x}, {y}, {z}) for label {text} ({artist_type})"
                # )
                # Handle the removal of the annotation if it already exists and is clicked again
                abord = False
                for annotation in ax.texts:
                    annotation_text = annotation.get_text()
                    if (annotation_text == text) and (
                        text in annotation_texts[artist_type]
                    ):
                        annotation.remove()
                        annotation_texts[artist_type].remove(text)
                        abord = True
                if abord:
                    return
                # Add a random jittering to the coordinates of the annotation for the "column" type.
                # Useful to avoid overlapping of the annotations when the points are overlapping.
                if artist_type == "column":
                    stdev = np.min([stdev_x, stdev_y, stdev_z])
                    np.random.seed(42)
                    x += np.random.randn() * stdev
                    y += np.random.randn() * stdev
                    z += np.random.randn() * stdev
                # print(f"Text shown at ({x}, {y}, {z}) for label {text}")
                # Add the annotation to the plot with the selected color based on type
                ax.text(
                    x,
                    y,
                    z,
                    text,
                    fontsize=10,
                    color=COLORS[1] if artist_type == "column" else COLORS[0],
                    backgroundcolor="#081512",
                    fontweight="bold",
                )
                # Add the annotation to the list of annotations
                annotation_texts[artist_type].append(text)

        # Get the coordinates of the point clicked
        handle_annotations(event.artist, event.ind)
        # redraw the canvas
        fig.canvas.draw()

    # Connect the pick_event_method function to the figure
    fig.canvas.mpl_connect("pick_event", pick_event_method)
    # Return the figure
    return fig
