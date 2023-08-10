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

"""Module to plot the initial matching results between the input dataset columns and the target CDE codes."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        "ytick.major.pad": 8,
    }
)


def heatmap_matching(
    figure, matrix, inputDatasetColumns, targetCDECodes, matchingMethod
):
    """Render a heatmap of the initial matching results between the input dataset columns and the target CDE codes.

    Parameters
    ----------
    figure: matplotlib.figure.Figure
        Figure to render the heatmap of the matching results.

    matrix: numpy.ndarray
        Similarity / distance matrix of the matching results.

    inputDatasetColumns: list
        List of the input dataset columns. Used as ytick labels.

    targetCDECodes: list
        List of the target CDE codes. Used as xtick labels.

    matchingMethod: str
        Matching method used to generate the similarity / distance matrix.
        Used to generate the title of the figure.
    """
    # Generate the figure
    left, bottom, width, height = 0.2, 0.1, 0.8, 0.2
    ax = figure.add_axes([left, bottom, width, height])
    xtickLabels = targetCDECodes
    ytickLabels = inputDatasetColumns
    sns.heatmap(
        matrix,
        ax=ax,
        xticklabels=xtickLabels,
        yticklabels=ytickLabels,
        annot=True,
        fmt=".2f",
        cmap="viridis",
    )
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    distance_type = (
        r"$(1 - 0.01 * \mathrm{LevenshteinRatio})$"
        if matchingMethod == "fuzzy"
        else "Cosine distance"
    )
    title = (
        f"Distances for the most {matrix.shape[1]} similar CDE codes\n"
        f"(method: {matchingMethod}, distance: {distance_type})"
    )
    ax.set_title(title)
    plt.xticks(rotation=75)
    plt.yticks(rotation=90)
    return figure
