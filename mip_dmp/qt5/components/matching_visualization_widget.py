"""Class for the widget that supports the visualization of the initial automated mapping matches."""

# External imports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide2.QtWidgets import QVBoxLayout, QWidget, QComboBox

# Internal imports
from mip_dmp.plot.embedding import scatterplot_embeddings


class MappingMatchVisualizationWidget(QWidget):
    """Class for the widget that supports the visualization of the automated column / CDE code matches."""

    def __init__(self, parent=None):
        """Initialize the widget. If parent is `None`, the widget renders as a separate window."""
        super(MappingMatchVisualizationWidget, self).__init__(parent)
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
        self.figure = plt.figure(figsize=(6, 6))
        self.canvas = FigureCanvas(self.figure)
        self.widgetLayout.addWidget(self.canvas)

    def set_word_list(self, wordList):
        """Set the list of words that can be visualized in the 3D scatter plot.

        wordList: list
            List of words to visualize in the 3D scatter plot
        """
        self.wordComboBox.clear()
        self.wordComboBox.addItems(wordList)

    def generate_embedding_figure(self, inputDataset, targetCDEs, matchingMethod):
        """Generate 3D scatter plot showing the embedding vectors of the words reduced with t-SNE.

        inputDataset: pandas.DataFrame
            Pandas Dataframe containing the input dataset

        targetCDEs: pandas.DataFrame
            Pandas Dataframe containing the target CDEs Metadata Schema

        matchingMethod: str
            Matching method. Can be "glove" or "chars2vec"
        """
        scatterplot_embeddings(
            self.figure,
            inputDataset,
            targetCDEs,
            matchingMethod,
            self.dimReductionMethodComboBox.currentText(),
        )
        self.figure.canvas.draw()
