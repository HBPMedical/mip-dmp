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
        self.figure = plt.figure(figsize=(6, 6))
        self.canvas = FigureCanvas(self.figure)
        self.widgetLayout.addWidget(self.canvas)

    def generate_embedding_figure(self, inputDataset, targetCDEs, matchingMethod):
        """Generate 3D scatter plot showing the embedding vectors of the words reduced with t-SNE.

        inputDataset: pandas.DataFrame
            Pandas Dataframe containing the input dataset

        targetCDEs: pandas.DataFrame
            Pandas Dataframe containing the target CDEs Metadata Schema

        matchingMethod: str
            Matching method. Can be "glove" or "chars2vec"
        """
        scatterplot_embeddings(self.figure, inputDataset, targetCDEs, matchingMethod)
        self.figure.canvas.draw()
