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

"""Module that defines the class for the widget that supports the visualization of the distances obtained by the automated mapping matches for the n most similar CDE codes."""

# External imports
import os
import matplotlib.pyplot as plt
import pkg_resources
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)

from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QVBoxLayout, QWidget, QComboBox

# Internal imports
from mip_dmp.plot.matching import heatmap_matching
from mip_dmp.process.matching import make_distance_vector


WINDOW_NAME = "Column /CDE Match Distance Visualization"


class MatchingVisualizationWidget(QWidget):
    """Class for the widget that supports the visualization of the distances / similarity measures obtained by the automated mapping matches for the n most similar CDE codes."""

    def __init__(
        self,
        inputDatasetColumns=None,
        targetCDECodes=None,
        matchedCdeCodes=None,
        matchingMethod=None,
        parent=None,
    ):
        """Initialize the widget. If parent is `None`, the widget renders as a separate window.

        inputDatasetColumns: list
            List of the input dataset columns.

        targetCDECodes: list
            List of the target CDE codes.

        matchedCdeCodes: dict
            Dictionary with the matched CDE codes in the following format::

                {
                    "input_dataset_column_1": {
                        "words": [ "cde_code_1", "cde_code_2", ... ],
                        "distances": [ distance_1, distance_2, ... ],
                        "embeddings": [ embedding_1, embedding_2, ... ]
                    },
                    "input_dataset_column_2": {
                        "words": [ "cde_code_1", "cde_code_2", ... ],
                        "distances": [ distance_1, distance_2, ... ],
                        "embeddings": [ embedding_1, embedding_2, ... ]
                    },
                    ...
                }

        matchingMethod: str
            String with the matching method. Can be one of the following:
            - `fuzzy`
            - `chars2vec`
            - `glove`
        """
        super(MatchingVisualizationWidget, self).__init__(parent)
        self.adjustWindow()
        self.widgetLayout = QVBoxLayout()
        self.setLayout(self.widgetLayout)
        # Set up the combo box for selecting the word to visualize
        # its dimensionaly reduced embedding vector in the 3D scatter plot
        # with the ones of the CDE codes
        self.wordComboBox = QComboBox()
        self.widgetLayout.addWidget(self.wordComboBox)
        # Set up the matplotlib figure and canvas
        self.canvasLayout = QVBoxLayout()
        self.figure = plt.figure(figsize=(12, 12))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvasLayout.addWidget(self.canvas)
        self.canvasLayout.addWidget(self.toolbar)
        self.widgetLayout.addLayout(self.canvasLayout, stretch=1)
        # Initialize the class attributes (if set)
        self.inputDatasetColumns = (
            inputDatasetColumns if inputDatasetColumns else list()
        )
        self.targetCDECodes = targetCDECodes if targetCDECodes else list()
        self.matchedCdeCodes = matchedCdeCodes if matchedCdeCodes else dict()
        self.matchingMethod = matchingMethod if matchingMethod else None
        # Connect the combo box to the function that generates the heatmap
        self.wordComboBox.currentIndexChanged.connect(self.generate_heatmap_figure)

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

    def set_wordcombobox_items(self, wordList):
        """Set the items of the word combo box.

        Parameters
        ----------
        wordList: list
            List of the words to add to the combo box.
        """
        self.wordComboBox.clear()
        self.wordComboBox.addItems(wordList)

    def generate_heatmap_figure(self):
        """Generate a heatmap figure with seaborn that shows the similarity / distance matrix of the input dataset columns and the target CDE codes."""
        # Generate the distance vector
        distanceVector = make_distance_vector(
            self.matchedCdeCodes, self.wordComboBox.currentText()
        )
        # Generate the heatmap
        self.figure.clear()
        self.figure = heatmap_matching(
            self.figure,
            distanceVector,
            [
                self.wordComboBox.currentText()
            ],  # give the input dataset column only for y labels
            self.matchedCdeCodes[self.wordComboBox.currentText()][
                "words"
            ],  # give the n most similar CDE codes for x labels
            self.matchingMethod,
        )
        # Draw the figure
        self.figure.canvas.draw()
