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

"""Module that defines the class dedicated to the widget that supports the visualization of the initial automated mapping matches via embedding."""

# External imports
import os
import numpy as np
import matplotlib.pyplot as plt
import pkg_resources
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QVBoxLayout, QWidget, QComboBox

# Internal imports
from mip_dmp.plot.embedding import scatterplot_embeddings
from mip_dmp.process.embedding import generate_embeddings, reduce_embeddings_dimension


# Constants
WINDOW_NAME = "Word Embedding Matches Visualization"
NB_KEPT_MATCHES = 15

class WordEmbeddingVisualizationWidget(QWidget):
    """Class for the widget that supports the visualization of the automated column / CDE code matches via embedding."""

    def __init__(self, parent=None):
        """Initialize the widget. If parent is `None`, the widget renders as a separate window."""
        super(WordEmbeddingVisualizationWidget, self).__init__(parent)
        self.adjustWindow()
        self.widgetLayout = QVBoxLayout()
        self.setLayout(self.widgetLayout)
        # Set up the combo box for selecting the dimensionality reduction method
        self.dimReductionMethodComboBox = QComboBox()
        self.dimReductionMethodComboBox.addItems(["tsne", "pca"])
        self.widgetLayout.addWidget(self.dimReductionMethodComboBox)
        # Set up the combo box for selecting the word to visualize
        # its dimensionaly reduced embedding vector in the 3D scatter plot
        # with the ones of the CDE codes
        self.wordComboBox = QComboBox()
        self.widgetLayout.addWidget(self.wordComboBox)
        # Set up the matplotlib figure and canvas
        self.canvasLayout = QVBoxLayout()
        self.figure = plt.figure(figsize=(6, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvasLayout.addWidget(self.canvas)
        self.canvasLayout.addWidget(self.toolbar)
        self.widgetLayout.addLayout(self.canvasLayout, stretch=1)
        # Initialize the class attributes
        self.inputDatasetColumns = list()
        self.targetCDECodes = list()
        self.inputDatasetColumnEmbeddings = list()
        self.targetCDECodeEmbeddings = list()
        self.matchedCdeCodes = dict()
        self.matchingMethod = None
        self.embeddings = dict()
        # Connect signals to slots
        self.dimReductionMethodComboBox.currentIndexChanged.connect(
            self.generate_embedding_figure
        )
        self.wordComboBox.currentIndexChanged.connect(self.generate_embedding_figure)

    def adjustWindow(self):
        """Adjust the window size, Qt Style Sheet, and title.

        Parameters
        ----------
        mainWindow : QMainWindow
            The main window of the application.
        """
        # Adjust the window size
        # self.resize(1280, 720)
        # Set the window Qt Style Sheet
        styleSheetFile = pkg_resources.resource_filename(
            "mip_dmp", os.path.join("qt5", "assets", "stylesheet.qss")
        )
        with open(styleSheetFile, "r") as fh:
            self.setStyleSheet(fh.read())
        # Set the window title
        self.setWindowTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", f"{WINDOW_NAME}", None)
        )

    def set_word_list(self, wordList):
        """Set the list of words that can be visualized in the 3D scatter plot.

        wordList: list
            List of words to visualize in the 3D scatter plot
        """
        self.wordComboBox.clear()
        self.wordComboBox.addItems(wordList)

    def set_matching_method(self, matchingMethod):
        """Set the matching method.

        matchingMethod: str
            Matching method. Can be "glove" or "chars2vec"
        """
        self.matchingMethod = matchingMethod

    def generate_embeddings(
        self, inputDatasetColumns: list, targetCDECodes: list, matchingMethod: str
    ):
        """Generate the embeddings of the columns and CDE codes.

        Set the input dataset columns (`self.inputDatasetColumns`), the target CDE codes (`self.targetCDECodes`),
        the input dataset column embeddings (`self.inputDatasetColumnEmbeddings`) and the target CDE code embeddings
        (`self.targetCDECodeEmbeddings`).

        The embeddings are generated using the specified matching method (`matchingMethod`).
        The matching method can be "glove" or "chars2vec".

        inputDatasetColumns: list
            List of the input dataset columns.

        targetCDECodes: list
            List of the target CDE codes.

        matchingMethod: str
            Matching method. Can be "glove" or "chars2vec"
        """
        self.set_matching_method(matchingMethod)
        self.inputDatasetColumns = inputDatasetColumns
        self.targetCDECodes = targetCDECodes
        self.inputDatasetColumnEmbeddings = generate_embeddings(
            inputDatasetColumns, matchingMethod
        )
        self.targetCDECodeEmbeddings = generate_embeddings(
            targetCDECodes, matchingMethod
        )

    def set_embeddings(
        self,
        inputDatasetColumnEmbeddings: list,
        inputDatasetColumns: list,
        targetCDECodeEmbeddings: list,
        targetCDECodes: list,
        matchedCdeCodes: dict,
        matchingMethod: str,
    ):
        """Set the input dataset column and target CDE code embeddings.

        inputDatasetColumnEmbeddings: list
            List of the input dataset column embeddings.

        inputDatasetColumns: list
            List of the input dataset columns.

        targetCDECodeEmbeddings: list
            List of the target CDE code embeddings.

        targetCDECodes: list
            List of the target CDE codes.

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

        matchingMethod: str
            Matching method. Can be "glove" or "chars2vec".
        """
        self.set_matching_method(matchingMethod)
        self.inputDatasetColumnEmbeddings = inputDatasetColumnEmbeddings
        self.inputDatasetColumns = inputDatasetColumns
        self.targetCDECodeEmbeddings = targetCDECodeEmbeddings
        self.targetCDECodes = targetCDECodes
        self.matchedCdeCodes = matchedCdeCodes
        # Reduce embeddings dimension to 3 components via t-SNE or PCA for visualization
        dim_reduction_method = self.dimReductionMethodComboBox.currentText()
        x, y, z = reduce_embeddings_dimension(
            self.inputDatasetColumnEmbeddings + self.targetCDECodeEmbeddings,
            reduce_method=dim_reduction_method,
        )
        # Set the dictionary with the embeddings and their labels, format expected
        # by the scatterplot function
        self.embeddings = dict(
            {
                "x": x,
                "y": y,
                "z": z,
                "label": self.inputDatasetColumns + self.targetCDECodes,
                "type": (
                    ["column"] * len(self.inputDatasetColumns)
                    + ["cde"] * len(self.targetCDECodes)
                ),
            }
        )

    def set_wordcombobox_items(self, wordList):
        """Set the items of the word combo box.

        wordList: list
            List of words to visualize in the combo box of the widget
            that controls the selection of the word to visualize in the
            3D scatter plot.
        """
        self.wordComboBox.clear()
        self.wordComboBox.addItems(wordList)

    def generate_embedding_figure(self):
        """Generate 3D scatter plot showing dimensionality-reduced embedding vectors of the words."""

        if (
            len(self.inputDatasetColumnEmbeddings) > 0
            and len(self.targetCDECodeEmbeddings) > 0
        ):
            matchedCdeCodes = self.matchedCdeCodes.copy()
            # Keep only the NB_KEPT_MATCHES most similar CDE codes for a variable
            for key in ["words", "distances"]:
                matchedCdeCodes[self.wordComboBox.currentText()][
                    key
                ] = matchedCdeCodes[self.wordComboBox.currentText()][
                    key
                ][:NB_KEPT_MATCHES]
            embeddings = self.embeddings.copy()
            embeddings = [embedding_vector[:NB_KEPT_MATCHES] for embedding_vector in embeddings]
            # Generate 3D scatter plot
            scatterplot_embeddings(
                self.figure,
                self.embeddings,
                self.matchedCdeCodes,
                self.wordComboBox.currentText(),
            )
            # Draw the figure
            self.figure.canvas.draw()
