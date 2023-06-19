"""Class for the main window of the MIP Dataset Mapper UI application."""

# External imports
import ast
import os
import json
from pathlib import Path
import pandas as pd
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QRect, QMetaObject, QCoreApplication, QSize
from PySide2.QtWidgets import (
    QAction,
    QWidget,
    QGridLayout,
    QSplitter,
    QGroupBox,
    QTableView,
    QFormLayout,
    QPushButton,
    QLabel,
    QStatusBar,
    QFileDialog,
    QMessageBox,
    QAbstractItemView,
    QComboBox,
    QToolBar,
    QSizePolicy,
    QLineEdit,
    QHeaderView,
    QHBoxLayout,
    QVBoxLayout,
    QInputDialog,
)
import pkg_resources

# Internal imports
from mip_dmp.io import load_mapping_json
from mip_dmp.process.mapping import (
    map_dataset,
    MAPPING_TABLE_COLUMNS,
)
from mip_dmp.process.matching import match_columns_to_cdes
from mip_dmp.qt5.model.table_model import (
    # NoEditorDelegate,
    PandasTableModel,
)
from mip_dmp.qt5.components.embedding_visualization_widget import (
    WordEmbeddingVisualizationWidget,
)
from mip_dmp.qt5.components.matching_visualization_widget import (
    MatchingVisualizationWidget,
)

# Constants
WINDOW_NAME = "MIP Dataset Mapper"


class MIPDatasetMapperWindow(object):
    """Class for the main window of the MIP Dataset Mapper UI application."""

    __slots__ = [
        "__weakref__",
        "centralWidgetGridLayout",
        "centralWidgetSplitter",
        "centralwidget",
        "columnsCDEsMappingGroupBox",
        "columnsCDEsMappingGroupBoxLayout",
        "columnsCDEsMappingSplitter",
        "inputDatasetFormLayout",
        "inputDatasetFormLayoutWidget",
        "inputDatasetGroupBox",
        "inputDatasetGroupBoxLayout",
        "inputDatasetLoadButton",
        "inputDatasetPathLabel",
        "inputDatasetTableView",
        "leftCentralWidgetSplitter",
        "mapButton",
        "mappingFilePathLabel",
        "mappingFormLayout",
        "mappingFormLayoutWidget",
        "mappingLoadButton",
        "mappingSaveButton",
        "mappingCheckButton",
        "mappingTableView",
        "outputDirectoryLabel",
        "outputDirectorySelectButton",
        "outputFilenameLabel",
        "outputFilenameSelectButton",
        "outputFormLayout",
        "outputFormLayoutWidget",
        "outputGroupBox",
        "outputGroupBoxLayout",
        "rightCentralWidgetSplitter",
        "targetCDEsFormLayout",
        "targetCDEsFormLayoutWidget",
        "targetCDEsGroupBox",
        "targetCDEsGroupBoxLayout",
        "targetCDEsLoadButton",
        "targetCDEsPathLabel",
        "targetCDEsTableView",
        "inputDatasetPath",
        "inputDataset",
        "inputDatasetColumns",
        "inputDatasetPandasModel",
        "targetCDEsPath",
        "targetCDEs",
        "targetCDEsPandasModel",
        "mappingFilePath",
        "columnsCDEsMappingData",
        "columnsCDEsMappingPandasModel",
        "mappingTableRowUpdateGroupBox",
        "mappingTableRowUpdateGroupBoxLayout",
        "mappingRowIndex",
        "mappingTableViewWidget",
        "mappingTableViewLayout",
        "mappingTableViewAddDeleteRowWidget",
        "mappingTableViewAddDeleteRowLayout",
        "mappingTableViewAddRowButton",
        "mappingTableViewDeleteRowButton",
        "datasetColumn",
        "cdeCode",
        "cdeType",
        "transformType",
        "transform",
        "matchedCdeCodes",
        "updateMappingRowButton",
        "outputDirectoryPath",
        "outputFilename",
        "statusbar",
        "toolBar",
        "mappingInitLabel",
        "initMatchingMethod",
        "mappingInitButton",
        "embeddingVizButton",
        "embeddingFigure",
        "embeddingWidget",
        "embeddingWidgetLayout",
        "embeddingCanvas",
        "inputDatasetColumnEmbeddings",
        "targetCDEsEmbeddings",
        "matchingVizButton",
        "matchingWidget",
    ]

    def __init__(self, mainWindow):
        """Initialize the main window of the MIP Dataset Mapper UI application.

        Parameters
        ----------
        mainWindow : QMainWindow
            The main window of the application.
        """
        # Adjust the window size, Qt Style Sheet, and title
        self.adjustWindow(mainWindow)
        # Create the UI components
        self.createComponents(mainWindow)
        # Create the tool bar
        self.createToolBar(mainWindow)
        # Add click listener functions to the Button elements
        self.connectButtons()
        # Add Widgets to the layouts
        self.adjustWidgetsAndLayouts()
        # Set the central widget
        mainWindow.setCentralWidget(self.centralwidget)
        # Set the status and tool bars
        mainWindow.setStatusBar(self.statusbar)
        mainWindow.addToolBar(self.toolBar)
        # Search recursively for all child objects of the given object, and
        # connect matching signals from them to slots of object
        QMetaObject.connectSlotsByName(mainWindow)
        # Set the initial state of the UI where the save mapping and
        # map buttons are disabled
        self.disableMappingInitItems()
        self.disableMappingMapButtons()

    def adjustWindow(self, mainWindow):
        """Adjust the window size, Qt Style Sheet, and title.

        Parameters
        ----------
        mainWindow : QMainWindow
            The main window of the application.
        """
        if not mainWindow.objectName():
            mainWindow.setObjectName(f"{WINDOW_NAME}")
        mainWindow.resize(1280, 720)
        # Set the window Qt Style Sheet
        styleSheetFile = pkg_resources.resource_filename(
            "mip_dmp", os.path.join("qt5", "assets", "stylesheet.qss")
        )
        with open(styleSheetFile, "r") as fh:
            mainWindow.setStyleSheet(fh.read())
        # Set the window icon
        # mainWindow.setWindowIcon(QIcon(":/images/mip_logo.png"))
        # Set the window title
        mainWindow.setWindowTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", f"{WINDOW_NAME}", None)
        )

    def createComponents(self, mainWindow):
        """Create the UI components.

        Parameters
        ----------
        mainWindow : QMainWindow
            The main window of the application.
        """
        # Initialize the central widget
        self.centralwidget = QWidget(mainWindow)
        self.centralWidgetGridLayout = QGridLayout(self.centralwidget)
        # Initialize the different main splitters
        self.centralWidgetSplitter = QSplitter(Qt.Horizontal)
        self.leftCentralWidgetSplitter = QSplitter(Qt.Vertical)
        self.rightCentralWidgetSplitter = QSplitter(Qt.Vertical)
        # Initialize components of the input dataset group box (top left)
        self.createInputDatasetComponents(mainWindow)
        # Initialize components of the target CDEs group box (bottom left)
        self.createTargetCDEsComponents(mainWindow)
        # Initialize components of the columns CDEs mapping group box (top right)
        self.createMappingComponents(mainWindow)
        # Create the status bar
        self.statusbar = QStatusBar(mainWindow)

    def createToolBar(self, mainWindow):
        """Create the tool bar."""
        # Initialize the tool bar
        self.toolBar = QToolBar()
        self.toolBar.setIconSize(QSize(48, 48))
        self.toolBar.setFloatable(True)
        # Add the load dataset / CDE file buttons to the tool bar
        inputDatasetToolLabel = QLabel("1. Source Dataset:")
        inputDatasetToolLabel.setStyleSheet(
            "QLabel { font-weight: bold; color: #222222;}"
        )
        self.toolBar.addWidget(inputDatasetToolLabel)
        self.toolBar.addAction(self.inputDatasetLoadButton)
        # Add a spacer to the tool bar
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(spacer)
        # Add a separator to the tool bar
        self.toolBar.addSeparator()
        # Add the load target CDEs file button to the tool bar
        targetCDEsToolLabel = QLabel("2. Target Schema:")
        targetCDEsToolLabel.setStyleSheet(
            "QLabel { font-weight: bold; color: #222222;}"
        )
        self.toolBar.addWidget(targetCDEsToolLabel)
        self.toolBar.addAction(self.targetCDEsLoadButton)
        # Add a spacer to the tool bar
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(spacer2)
        # Add a separator to the tool bar
        self.toolBar.addSeparator()
        # Add the button related to mapping table initialization to the tool bar
        mappingInitLabel = QLabel("(3). Mapping Initialization:")
        mappingInitLabel.setStyleSheet("QLabel { font-weight: bold; color: #222222;}")
        self.initMatchingMethod = QComboBox()
        icon = pkg_resources.resource_filename(
            "mip_dmp", os.path.join("qt5", "assets", "down_arrow.png")
        )
        self.initMatchingMethod.setStyleSheet(
            f"QComboBox::down-arrow {{ image: url({icon}); height: 16px; width: 16px; }}"
        )
        self.initMatchingMethod.addItems(["fuzzy", "glove", "chars2vec"])
        self.initMatchingMethod.setGeometry(QRect(0, 0, 100, 30))
        self.toolBar.addWidget(mappingInitLabel)
        self.toolBar.addWidget(self.initMatchingMethod)
        self.mappingInitButton = QAction(
            QIcon(
                pkg_resources.resource_filename(
                    "mip_dmp", os.path.join("qt5", "assets", "init_mapping.png")
                )
            ),
            "Initialize Mapping",
            mainWindow,
        )
        self.toolBar.addAction(self.mappingInitButton)
        self.matchingVizButton = QAction(
            QIcon(
                pkg_resources.resource_filename(
                    "mip_dmp", os.path.join("qt5", "assets", "heatmap_matching.png")
                )
            ),
            "Visualize Column /CDE Match Distances",
            mainWindow,
        )
        self.toolBar.addAction(self.matchingVizButton)
        self.embeddingVizButton = QAction(
            QIcon(
                pkg_resources.resource_filename(
                    "mip_dmp", os.path.join("qt5", "assets", "plot_embedding.png")
                )
            ),
            "Visualize Word Embedding Matches in 3D (Enabled only for GloVe and Chars2Vec methods)",
            mainWindow,
        )
        self.toolBar.addAction(self.embeddingVizButton)
        # Add a spacer to the tool bar
        spacer3 = QWidget()
        spacer3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(spacer3)
        # Add a separator to the tool bar
        self.toolBar.addSeparator()
        # Add the load / save mapping file buttons to the tool bar
        mappingToolLabel = QLabel("4. Mapping Check / Save / Load:")
        mappingToolLabel.setStyleSheet("QLabel { font-weight: bold; color: #222222;}")
        self.toolBar.addWidget(mappingToolLabel)
        self.toolBar.addAction(self.mappingCheckButton)
        self.toolBar.addAction(self.mappingSaveButton)
        self.toolBar.addAction(self.mappingLoadButton)
        # Add a spacer to the tool bar
        spacer4 = QWidget()
        spacer4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(spacer4)
        # Add a separator to the tool bar
        self.toolBar.addSeparator()
        # Add the map button to the tool bar
        actionsLabel = QLabel("5. Map:")
        actionsLabel.setStyleSheet("QLabel { font-weight: bold; color: #222222;}")
        self.toolBar.addWidget(actionsLabel)
        self.mapButton = QAction(
            QIcon(
                pkg_resources.resource_filename(
                    "mip_dmp", os.path.join("qt5", "assets", "map.png")
                )
            ),
            "Map",
            mainWindow,
        )
        self.toolBar.addAction(self.mapButton)

    def createInputDatasetComponents(self, mainWindow):
        """Create the components of the input dataset group box."""
        self.inputDatasetGroupBox = QGroupBox(self.centralwidget)
        # Set the layout of the group box
        self.inputDatasetGroupBoxLayout = QGridLayout()
        # Set the table view
        self.inputDatasetTableView = QTableView(self.inputDatasetGroupBox)
        self.inputDatasetTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.inputDatasetTableView.setGeometry(QRect(10, 71, 341, 281))
        # Set the form layout with button to load the dataset
        self.inputDatasetFormLayoutWidget = QWidget(self.inputDatasetGroupBox)
        self.inputDatasetFormLayoutWidget.setGeometry(QRect(10, 30, 341, 31))
        self.inputDatasetFormLayout = QFormLayout(self.inputDatasetFormLayoutWidget)
        self.inputDatasetFormLayout.setContentsMargins(0, 0, 0, 0)
        self.inputDatasetLoadButton = QAction(
            QIcon(
                pkg_resources.resource_filename(
                    "mip_dmp", "qt5/assets/load_dataset.png"
                )
            ),
            "Load dataset",
            mainWindow,
        )
        self.inputDatasetLoadButton.setToolTip("Load source dataset (.csv format)")
        self.inputDatasetPathLabel = QLabel(self.inputDatasetFormLayoutWidget)
        # Set text of the components
        self.inputDatasetGroupBox.setTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Source Dataset", None)
        )
        self.inputDatasetPathLabel.setText(
            QCoreApplication.translate(
                f"{WINDOW_NAME}",
                "<Please load a source dataset file in .csv format...>",
                None,
            )
        )

    def createTargetCDEsComponents(self, mainWindow):
        """Create the components of the target CDEs group box."""
        self.targetCDEsGroupBox = QGroupBox(self.centralwidget)
        # Set the layout of the group box
        self.targetCDEsGroupBoxLayout = QGridLayout()
        # Set the table view
        self.targetCDEsTableView = QTableView(self.targetCDEsGroupBox)
        self.targetCDEsTableView.setGeometry(QRect(10, 70, 341, 101))
        self.targetCDEsTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Set the form layout with button to load the CDEs file
        self.targetCDEsFormLayoutWidget = QWidget(self.targetCDEsGroupBox)
        self.targetCDEsFormLayoutWidget.setGeometry(QRect(10, 30, 341, 31))
        self.targetCDEsFormLayout = QFormLayout(self.targetCDEsFormLayoutWidget)
        self.targetCDEsFormLayout.setContentsMargins(0, 0, 0, 0)
        self.targetCDEsLoadButton = QAction(
            QIcon(
                pkg_resources.resource_filename("mip_dmp", "qt5/assets/load_cdes.png")
            ),
            "Load CDE file",
            mainWindow,
        )
        self.targetCDEsLoadButton.setToolTip(
            "Load CDEs metadata schema file (.xlxs format)"
        )
        self.targetCDEsPathLabel = QLabel(self.targetCDEsFormLayoutWidget)
        # Set text of the components
        self.targetCDEsGroupBox.setTitle(
            QCoreApplication.translate(
                f"{WINDOW_NAME}", "Target CDEs Metadata Schema", None
            )
        )
        self.targetCDEsPathLabel.setText(
            QCoreApplication.translate(
                f"{WINDOW_NAME}",
                "<Please load a CDEs metadata schema file in .xlxs format>",
                None,
            )
        )

    def createMappingComponents(self, mainWindow):
        """Create the components of the mapping group box."""
        self.columnsCDEsMappingGroupBox = QGroupBox(self.centralwidget)
        # Set the layout of the group box
        self.columnsCDEsMappingGroupBoxLayout = QGridLayout()
        # Set the form to load the mapping file
        self.mappingFormLayoutWidget = QWidget(self.columnsCDEsMappingGroupBox)
        self.mappingFormLayoutWidget.setGeometry(QRect(10, 30, 371, 31))
        self.mappingFormLayout = QFormLayout(self.mappingFormLayoutWidget)
        self.mappingFormLayout.setContentsMargins(0, 0, 0, 0)
        self.mappingLoadButton = QAction(
            QIcon(
                pkg_resources.resource_filename(
                    "mip_dmp", "qt5/assets/load_mapping.png"
                )
            ),
            "Load mapping file",
            mainWindow,
        )
        self.mappingLoadButton.setToolTip(
            "Load Columns / CDEs mapping file (.json format)"
        )
        self.mappingFilePathLabel = QLabel(self.mappingFormLayoutWidget)
        # Set the splitter for the mapping table and the new entry form
        self.columnsCDEsMappingSplitter = QSplitter(Qt.Vertical)
        self.mappingTableViewWidget = QWidget(self.columnsCDEsMappingGroupBox)
        self.mappingTableViewLayout = QVBoxLayout()
        # Set the mapping table
        self.mappingTableView = QTableView(self.columnsCDEsMappingGroupBox)
        self.mappingTableView.setGeometry(QRect(10, 70, 371, 231))
        self.mappingTableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.mappingTableView.horizontalHeader().setVisible(True)
        self.mappingTableViewAddDeleteRowWidget = QWidget(
            self.columnsCDEsMappingGroupBox
        )
        self.mappingTableViewAddDeleteRowLayout = QHBoxLayout()
        self.mappingTableViewAddRowButton = QPushButton(self.columnsCDEsMappingGroupBox)
        self.mappingTableViewAddRowButton.setToolTip(
            "Add a new row to the mapping table"
        )
        self.mappingTableViewAddRowButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Add", None)
        )
        self.mappingTableViewDeleteRowButton = QPushButton(
            self.columnsCDEsMappingGroupBox
        )
        self.mappingTableViewDeleteRowButton.setToolTip(
            "Delete the selected row from the mapping table"
        )
        self.mappingTableViewDeleteRowButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Delete", None)
        )
        # Create group box for entering a new entry to the mapping table
        self.mappingTableRowUpdateGroupBox = QGroupBox()
        # Create a form widget to edit row of mapping table
        self.createMappingTableRowViewComponents()
        self.mappingTableRowUpdateGroupBox.setTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Mapping Row Editor", None)
        )
        # Create the save button
        self.mappingSaveButton = QAction(
            QIcon(
                pkg_resources.resource_filename(
                    "mip_dmp", "qt5/assets/save_mapping.png"
                )
            ),
            "Save mapping file",
            mainWindow,
        )
        self.mappingSaveButton.setToolTip(
            "Save Columns / CDEs mapping file (.json format)"
        )
        self.mappingCheckButton = QAction(
            QIcon(
                pkg_resources.resource_filename(
                    "mip_dmp", "qt5/assets/check_mapping.png"
                )
            ),
            "Check Columns / CDEs mapping",
            mainWindow,
        )
        self.mappingCheckButton.setToolTip("Check Columns / CDEs mapping")
        # Set text of the components
        self.columnsCDEsMappingGroupBox.setTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Columns / CDEs Mapping", None)
        )
        self.mappingFilePathLabel.setText(
            QCoreApplication.translate(
                f"{WINDOW_NAME}",
                "<Please save/ load a Columns / CDEs mapping file in .json format...>",
                None,
            )
        )

    def createMappingTableRowViewComponents(self):
        """Create the components of the mapping table row editor group box."""
        # Create a form layout for the mapping group box
        self.mappingTableRowUpdateGroupBoxLayout = QFormLayout()
        # Setup the widgets
        self.mappingRowIndex = QLabel(self.columnsCDEsMappingGroupBox)
        self.datasetColumn = QLabel(self.columnsCDEsMappingGroupBox)
        self.cdeCode = QComboBox(self.columnsCDEsMappingGroupBox)
        self.cdeType = QLabel(self.columnsCDEsMappingGroupBox)
        self.transformType = QLabel(self.columnsCDEsMappingGroupBox)
        self.transform = QLineEdit(self.columnsCDEsMappingGroupBox)
        self.updateMappingRowButton = QPushButton(
            "Update row", self.columnsCDEsMappingGroupBox
        )
        # Add widgets to the form layout
        self.mappingTableRowUpdateGroupBoxLayout.addRow(
            QLabel("Mapping Table Row Index"), self.mappingRowIndex
        )
        self.mappingTableRowUpdateGroupBoxLayout.addRow(
            QLabel("Dataset Column"), self.datasetColumn
        )
        self.mappingTableRowUpdateGroupBoxLayout.addRow(
            QLabel("CDE Code"), self.cdeCode
        )
        self.mappingTableRowUpdateGroupBoxLayout.addRow(
            QLabel("CDE Type"), self.cdeType
        )
        self.mappingTableRowUpdateGroupBoxLayout.addRow(
            QLabel("Transform Type"), self.transformType
        )
        self.mappingTableRowUpdateGroupBoxLayout.addRow(
            QLabel("Transform"), self.transform
        )
        self.mappingTableRowUpdateGroupBoxLayout.addRow(
            QLabel(), self.updateMappingRowButton
        )

    def adjustWidgetsAndLayouts(self):
        """Add widgets to the layouts of the UI elements."""
        # Handle the splitters
        self.centralWidgetGridLayout.addWidget(self.centralWidgetSplitter, 0, 0, 1, 1)
        self.centralWidgetSplitter.addWidget(self.leftCentralWidgetSplitter)
        self.centralWidgetSplitter.addWidget(self.rightCentralWidgetSplitter)
        # Handle the widgets of the input dataset group box (top left)
        self.inputDatasetGroupBox.setLayout(self.inputDatasetGroupBoxLayout)
        self.inputDatasetGroupBoxLayout.addWidget(
            self.inputDatasetTableView, 0, 0, 1, 1
        )
        self.inputDatasetFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.inputDatasetPathLabel
        )
        self.inputDatasetGroupBoxLayout.addWidget(
            self.inputDatasetFormLayoutWidget, 1, 0, 1, 1
        )
        self.leftCentralWidgetSplitter.addWidget(self.inputDatasetGroupBox)
        # Handle the widgets of the target CDEs group box (bottom left)
        self.targetCDEsGroupBox.setLayout(self.targetCDEsGroupBoxLayout)
        self.targetCDEsGroupBoxLayout.addWidget(self.targetCDEsTableView, 0, 0, 1, 1)
        self.targetCDEsFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.targetCDEsPathLabel
        )
        self.targetCDEsGroupBoxLayout.addWidget(
            self.targetCDEsFormLayoutWidget, 1, 0, 1, 1
        )
        self.leftCentralWidgetSplitter.addWidget(self.targetCDEsGroupBox)
        # Handle the widgets of the columns CDEs mapping group box (right)
        self.columnsCDEsMappingGroupBox.setLayout(self.columnsCDEsMappingGroupBoxLayout)
        self.mappingFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.mappingFilePathLabel
        )
        self.columnsCDEsMappingGroupBoxLayout.addWidget(
            self.columnsCDEsMappingSplitter, 0, 0, 1, 1
        )
        self.mappingTableViewWidget.setLayout(self.mappingTableViewLayout)
        self.mappingTableViewLayout.addWidget(self.mappingTableView)
        self.mappingTableViewAddDeleteRowWidget.setLayout(
            self.mappingTableViewAddDeleteRowLayout
        )
        self.mappingTableViewAddDeleteRowLayout.addWidget(
            self.mappingTableViewAddRowButton
        )
        self.mappingTableViewAddDeleteRowLayout.addWidget(
            self.mappingTableViewDeleteRowButton
        )
        self.mappingTableViewLayout.addWidget(self.mappingTableViewAddDeleteRowWidget)
        self.columnsCDEsMappingSplitter.addWidget(self.mappingTableViewWidget)
        self.columnsCDEsMappingGroupBoxLayout.addWidget(
            self.mappingFormLayoutWidget, 1, 0, 1, 1
        )
        self.rightCentralWidgetSplitter.addWidget(self.columnsCDEsMappingGroupBox)
        self.mappingTableRowUpdateGroupBox.setLayout(
            self.mappingTableRowUpdateGroupBoxLayout
        )
        self.columnsCDEsMappingSplitter.addWidget(self.mappingTableRowUpdateGroupBox)

    def connectButtons(self):
        """Connect the buttons to their corresponding functions."""
        self.inputDatasetLoadButton.triggered.connect(self.loadInputDataset)
        self.targetCDEsLoadButton.triggered.connect(self.loadCDEsFile)
        self.mappingInitButton.triggered.connect(self.mappingMatch)
        self.mappingLoadButton.triggered.connect(self.loadMapping)
        self.mappingCheckButton.triggered.connect(self.checkMapping)
        self.mappingSaveButton.triggered.connect(self.saveMapping)
        self.mapButton.triggered.connect(self.map)
        self.updateMappingRowButton.clicked.connect(self.updateMappingTableRow)
        self.mappingTableViewAddRowButton.clicked.connect(self.addMappingTableRow)
        self.mappingTableViewDeleteRowButton.clicked.connect(self.deleteMappingTableRow)
        self.embeddingVizButton.triggered.connect(self.embeddingViz)
        self.matchingVizButton.triggered.connect(self.matchingViz)

    def embeddingViz(self):
        """Open the embedding visualization window."""
        self.embeddingWidget = WordEmbeddingVisualizationWidget()
        print(
            "Launch visualization widget with matching method: "
            f"{self.initMatchingMethod.currentText()}"
        )
        if self.initMatchingMethod.currentText() != "fuzzy":
            self.embeddingWidget.set_wordcombobox_items(self.inputDatasetColumns)
            self.embeddingWidget.set_embeddings(
                self.inputDatasetColumnEmbeddings,
                self.inputDatasetColumns,
                self.targetCDEsEmbeddings,
                list(self.targetCDEs["code"].unique()),
                self.matchedCdeCodes,
                self.initMatchingMethod.currentText(),
            )
            self.embeddingWidget.generate_embedding_figure()
            self.embeddingWidget.show()
        else:
            QMessageBox().warning(
                None,
                "Warning",
                "Embedding visualization is not available for fuzzy matching.",
            )

    def matchingViz(self):
        """Open the matching visualization window."""
        self.matchingWidget = MatchingVisualizationWidget(
            self.inputDatasetColumns,
            self.targetCDEs["code"].unique().tolist(),
            self.matchedCdeCodes,
            self.initMatchingMethod.currentText(),
            None,
        )
        self.matchingWidget.set_wordcombobox_items(self.inputDatasetColumns)
        print(
            "Launch matching visualization widget "
            f"(matching method: {self.initMatchingMethod.currentText()})"
        )
        self.matchingWidget.generate_heatmap_figure()
        self.matchingWidget.show()

    def addMappingTableRow(self):
        """Add a row to the mapping table."""
        # Show a dialog to enter the dataset column name
        # it is given the choice to select from the list of dataset columns.
        # If the user selects a column name from the list, the CDE code is
        # automatically filled in with the best match.
        datasetColumn, ok = QInputDialog().getItem(
            None,
            "Select dataset column to add to the mapping table",
            "Dataset column:",
            self.inputDatasetColumns,
            0,
            False,
        )
        if ok and datasetColumn is not None and datasetColumn != "":
            # Get the fuzzy matches list for the dataset column
            # and set the CDE code and type to the first match
            columnMatches = self.matchedCdeCodes[datasetColumn]["words"]
            cdeCode = columnMatches[0]
            cdeType = self.targetCDEs[self.targetCDEs["code"] == cdeCode][
                "type"
            ].unique()[0]
            if cdeType == "real" or cdeType == "integer":
                transformType = "scale"
                transform = "1.0"
            else:
                transformType = "map"
                transform = '{ "X": "Y", "Y": "X" }'
            newRow = {
                "dataset_column": datasetColumn,
                "cde_code": cdeCode,
                "cde_type": cdeType,
                "transform_type": transformType,
                "transform": transform,
            }
            # Use the loc method to add the new row to the DataFrame
            self.columnsCDEsMappingData.loc[len(self.columnsCDEsMappingData)] = newRow
            # Update the table
            self.mappingTableView.model().layoutChanged.emit()
            successMsg = (
                "New row for dataset column '{}' added to the mapping table!".format(
                    datasetColumn
                )
            )
            QMessageBox.information(None, "Success", successMsg)
            self.statusbar.showMessage(successMsg)
            self.statusbar.repaint()
        else:
            warnMsg = "No dataset column selected!"
            QMessageBox.warning(None, "Warning", warnMsg)
            self.statusbar.showMessage(warnMsg)
            self.statusbar.repaint()

    def deleteMappingTableRow(self):
        """Delete the selected row from the mapping table."""
        # Get the selected row index
        index = self.mappingTableView.selectedIndexes()[0]
        # Delete the row from the DataFrame
        self.columnsCDEsMappingData.drop(index=index.row(), inplace=True)
        self.columnsCDEsMappingData.reset_index(drop=True, inplace=True)
        # Update the table
        self.mappingTableView.model().layoutChanged.emit()
        successMsg = "Row {} deleted from the mapping table!".format(index.row())
        QMessageBox.information(None, "Success", successMsg)
        self.statusbar.showMessage(successMsg)
        self.statusbar.repaint()

    def initializeMappingEditForm(self, index):
        # Get the data for the current row and update the widgets in the form
        rowData = self.columnsCDEsMappingData.iloc[index.row(), :]
        self.mappingRowIndex.setText(str(index.row()))
        self.datasetColumn.setText(str(rowData["dataset_column"]))
        if self.matchedCdeCodes:
            columnMatches = self.matchedCdeCodes[rowData["dataset_column"]]["words"]
        else:
            columnMatches = self.targetCDEs["code"].unique().tolist()
        self.cdeCode.clear()
        self.cdeCode.addItems(columnMatches)
        ind = columnMatches.index(rowData["cde_code"])
        self.cdeCode.setCurrentIndex(ind)
        cdeType = self.targetCDEs[self.targetCDEs["code"] == columnMatches[ind]][
            "type"
        ].unique()[0]
        self.cdeType.setText(cdeType)
        if cdeType == "real" or cdeType == "integer":
            self.transformType.setText("scale")
            self.transform.setText(str(rowData["transform"]))
        else:
            self.transformType.setText("map")
            self.transform.setText(str(rowData["transform"]))

    def updateMappingEditForm(self, index):
        # Get the data for the current row and update the widgets in the form
        rowIndex = int(self.mappingRowIndex.text())
        rowData = self.columnsCDEsMappingData.iloc[rowIndex, :]
        if self.matchedCdeCodes:
            columnMatches = self.matchedCdeCodes[rowData["dataset_column"]]["words"]
        else:
            columnMatches = self.targetCDEs["code"].unique().tolist()
        cdeType = self.targetCDEs[self.targetCDEs["code"] == columnMatches[index]][
            "type"
        ].unique()[0]
        self.cdeType.setText(str(cdeType))
        if cdeType == "real" or cdeType == "integer":
            if self.cdeCode.currentText() == rowData["cde_code"]:
                self.transformType.setText("scale")
                self.transform.setText(str(rowData["transform"]))
            else:
                self.transformType.setText("scale")
                self.transform.setText("1.0")
        else:
            if self.cdeCode.currentText() == rowData["cde_code"]:
                self.transformType.setText("map")
                self.transform.setText(str(rowData["transform"]))
            else:
                self.transformType.setText("map")
                self.transform.setText('{ "X": "Y", "Y": "X" }')

    def updateMappingTableRow(self):
        # Get the data from the form
        rowIndex = int(self.mappingRowIndex.text())
        datasetColumn = self.datasetColumn.text()
        cdeCode = self.cdeCode.currentText()
        cdeType = self.cdeType.text()
        transformType = self.transformType.text()
        transform = self.transform.text()
        # Update the data in the table
        self.columnsCDEsMappingData.iloc[rowIndex, :] = [
            datasetColumn,
            cdeCode,
            cdeType,
            transformType,
            transform,
        ]
        # Update the table
        self.mappingTableView.model().layoutChanged.emit()

    def loadInputDataset(self):
        """Load the input dataset."""
        self.inputDatasetPath = QFileDialog.getOpenFileName(
            None, "Select the input dataset", "", "CSV files (*.csv)"
        )
        self.inputDatasetPathLabel.setText(self.inputDatasetPath[0])
        if not os.path.exists(self.inputDatasetPath[0]):
            self.inputDatasetPathLabel.setText(
                QCoreApplication.translate(
                    f"{WINDOW_NAME}", "<Please load a CSV file...>", None
                )
            )
            errMsg = (
                f"The input dataset file {self.inputDatasetPath[0]} does not exist. "
                "Please select a valid file!"
            )
            QMessageBox.warning(
                None,
                "Error",
                errMsg,
            )
            self.updateStatusbar(errMsg)
            self.disableMappingMapButtons()
        else:
            self.inputDataset = pd.read_csv(self.inputDatasetPath[0])
            self.inputDatasetColumns = self.inputDataset.columns.tolist()
            self.inputDatasetPandasModel = PandasTableModel(self.inputDataset)
            self.inputDatasetTableView.setModel(self.inputDatasetPandasModel)
            self.updateStatusbar(f"Loaded input dataset {self.inputDatasetPath[0]}")
            if hasattr(self, "targetCDEsPath") and os.path.exists(
                self.targetCDEsPath[0]
            ):
                self.initMapping()
                self.enableMappingButtons()
                self.enableMappingInitItems()
            else:
                self.disableMappingMapButtons()
                self.disableMappingInitItems()

    def loadCDEsFile(self):
        """Load the CDEs file."""
        self.targetCDEsPath = QFileDialog.getOpenFileName(
            None, "Select the CDEs file", "", "Excel files (*.xlsx)"
        )
        self.targetCDEsPathLabel.setText(self.targetCDEsPath[0])
        if not os.path.exists(self.targetCDEsPath[0]):
            self.targetCDEsPathLabel.setText(
                QCoreApplication.translate(
                    f"{WINDOW_NAME}", "<Please load a CDEs file in .xlxs>", None
                )
            )
            errMsg = (
                f"The CDEs file {self.targetCDEsPath[0]} does not exist. "
                "Please select a valid file!"
            )
            QMessageBox.warning(
                None,
                "Error",
                errMsg,
            )
            self.updateStatusbar(errMsg)
            self.disableMappingMapButtons()
        else:
            self.targetCDEs = pd.read_excel(self.targetCDEsPath[0])
            self.targetCDEsPandasModel = PandasTableModel(self.targetCDEs)
            self.targetCDEsTableView.setModel(self.targetCDEsPandasModel)
            successMsg = f"Loaded CDEs file {self.targetCDEsPath[0]}"
            self.updateStatusbar(successMsg)
            if hasattr(self, "inputDatasetPath") and os.path.exists(
                self.inputDatasetPath[0]
            ):
                self.initMapping()
                self.enableMappingInitItems()
                self.enableMappingButtons()
            else:
                self.disableMappingMapButtons()
                self.disableMappingInitItems()

    def loadMapping(self):
        """Load the mapping file."""
        self.mappingFilePath = QFileDialog.getOpenFileName(
            None, "Select the mapping file", "", "JSON files (*.json)"
        )
        self.mappingFilePathLabel.setText(self.mappingFilePath[0])
        if not os.path.exists(self.mappingFilePath[0]):
            self.mappingFilePathLabel.setText(
                QCoreApplication.translate(
                    f"{WINDOW_NAME}",
                    "<Please load an existing mapping json file...>",
                    None,
                )
            )
            errMsg = (
                f"The mapping file {self.mappingFilePath[0]} does not exist. "
                "Please select a valid file!"
            )
            QMessageBox.warning(
                None,
                "Error",
                errMsg,
            )
            self.updateStatusbar(errMsg)
            self.disableMappingMapButtons()
        else:
            try:
                # Load the mapping table file in JSON format
                self.columnsCDEsMappingData = load_mapping_json(self.mappingFilePath[0])
                print(f"Mapping loaded from {self.mappingFilePath[0]}")
                # Create a pandas model for the mapping table
                self.columnsCDEsMappingPandasModel = PandasTableModel(
                    self.columnsCDEsMappingData
                )
                # Set the model of the table view to the pandas model
                self.mappingTableView.setModel(self.columnsCDEsMappingPandasModel)
                self.mappingTableView.setSelectionBehavior(
                    self.mappingTableView.SelectRows
                )
                self.mappingTableView.setSelectionMode(
                    self.mappingTableView.SingleSelection
                )
                self.mappingTableView.setEditTriggers(
                    self.mappingTableView.NoEditTriggers
                )  # disable editing
                # Handle the mapping table view row selection changed signal
                self.mappingTableView.selectionModel().currentRowChanged.connect(
                    self.initializeMappingEditForm
                )
                # Select the first row of the mapping table view at the beginning
                indexRow = 0
                self.mappingTableView.selectRow(indexRow)
                # Handle the combox box current index changed signal for the CDE code column
                self.cdeCode.currentIndexChanged.connect(self.updateMappingEditForm)
                # Display a success message
                successMsg = (
                    f"Loaded mapping file {self.mappingFilePath[0]}. \n"
                    "Please Check the mapping, Save it and Click on the "
                    "Map button to map the input dataset."
                )
                QMessageBox.information(
                    None,
                    "Success",
                    successMsg,
                )
                self.updateStatusbar(successMsg)
            except ValueError as e:
                # Display an error message
                errMsg = (
                    f"The mapping file {self.mappingFilePath[0]} is not valid: {repr(e)} \n"
                    "Please select a valid file! "
                )
                QMessageBox.warning(
                    None,
                    "Error",
                    errMsg,
                )
                self.updateStatusbar(errMsg)
            self.disableMappingMapButtons()
            self.enableMappingButtons()

    def saveMapping(self):
        """Save the mapping file."""
        self.mappingFilePath = QFileDialog.getSaveFileName(
            None, "Select the mapping file", "", "JSON files (*.json)"
        )
        path = Path(self.mappingFilePath[0])
        if path.suffix != ".json":
            errMsg = (
                f"The mapping file {self.mappingFilePath[0]} does not have a .json extension. "
                "Please select a valid file!"
            )
            QMessageBox.warning(
                None,
                "Error",
                errMsg,
            )
            return
        # Create the directories if they do not exist
        os.makedirs(path.parent, exist_ok=True)
        # Convert the mapping data frame to a json file
        self.columnsCDEsMappingData.to_json(
            self.mappingFilePath[0], orient="records", indent=4
        )
        print(f"Mapping saved to {self.mappingFilePath[0]}")
        self.mappingFilePathLabel.setText(self.mappingFilePath[0])
        successMsg = f"Mapping saved to {self.mappingFilePath[0]}!"
        QMessageBox.information(
            None,
            "Success",
            successMsg,
        )
        self.updateStatusbar(successMsg)
        self.mapButton.setEnabled(True)

    def disableMappingMapButtons(self):
        """Disable the check / save / load mapping and map buttons."""
        self.mappingCheckButton.setEnabled(False)
        self.mappingSaveButton.setEnabled(False)
        self.mappingLoadButton.setEnabled(False)
        self.mapButton.setEnabled(False)

    def disableMappingInitItems(self):
        """Disable the mapping initialization items."""
        self.mappingInitButton.setEnabled(False)
        self.initMatchingMethod.setEnabled(False)
        self.embeddingVizButton.setEnabled(False)
        self.matchingVizButton.setEnabled(False)

    def enableMappingInitItems(self):
        """Enable the mapping initialization items."""
        self.mappingInitButton.setEnabled(True)
        self.initMatchingMethod.setEnabled(True)

    def enableMappingButtons(self):
        """Enable the check / save / load mapping and map buttons."""
        self.mappingCheckButton.setEnabled(True)
        # self.mappingSaveButton.setEnabled(True)
        self.mappingLoadButton.setEnabled(True)

    def checkMapping(self):
        """Check the mapping."""
        # Check if the mapping contains unique column / CDE pairs
        if len(self.columnsCDEsMappingData["cde_code"].unique()) != len(
            self.columnsCDEsMappingData["cde_code"]
        ):
            errMsg = (
                "The mapping is not valid. "
                "Please check it and remove any mapping row "
                "that might map multiple columns of the input dataset "
                "to the same CDE code!"
            )
            QMessageBox.warning(
                None,
                "Error: Duplicated mapped CDE code",
                errMsg,
            )
            self.updateStatusbar(errMsg)
            self.disableMappingMapButtons()
            return
        # if len(self.columnsCDEsMappingData["dataset_column"].unique()) != len(
        #     self.columnsCDEsMappingData["dataset_column"]
        # ):
        #     errMsg = (
        #         "The mapping is not valid. "
        #         "Please check it and remove any mapping row(s) "
        #         "that might map the same column(s) of "
        #         "the source dataset to multiple CDE codes!"
        #     )
        #     QMessageBox.warning(
        #         None,
        #         "Error: Duplicate Column / CDEs Pairs",
        #         errMsg,
        #     )
        #     self.updateStatusbar(errMsg)
        #     self.disableMappingMapButtons()
        #     return
        # Check if the mapping contains only valid CDE codes
        if self.columnsCDEsMappingData[
            self.columnsCDEsMappingData["cde_code"].isin(self.targetCDEs["code"])
        ].empty:
            errMsg = (
                "The mapping is not valid. "
                "Please check it and remove any invalid CDE code!"
            )
            QMessageBox.warning(
                None,
                "Error: Invalid CDE Codes",
                errMsg,
            )
            self.updateStatusbar(errMsg)
            self.disableMappingMapButtons()
            return
        # Check if the mapping transform is correctly formatted
        transformList = self.columnsCDEsMappingData["transform"].tolist()

        def is_invalid_map_transform(transform):
            """Check if the transform is an invalid map transform.

            We expect the transform to be a valid Python dictionary or
            a valid Python literal. If it is not, it is invalid.

            Parameters
            ----------
            transform : str
                The transform to check.
            """
            try:
                ast.literal_eval(f"{transform}")
                return False
            except ValueError:
                return True

        isInvalidTransformList = list(map(is_invalid_map_transform, transformList))
        if any(isInvalidTransformList):
            df_invalidtransform_with_index = pd.DataFrame(
                {
                    "transform": [
                        transformList[i]
                        for i in range(len(transformList))
                        if isInvalidTransformList[i]
                    ],
                    "mapping_row": [
                        i + 1
                        for i in range(len(transformList))
                        if isInvalidTransformList[i]
                    ],
                }
            )
            errMsg = (
                "The mapping is not valid. "
                "Please check it and correct "
                "any invalid transform!"
                f" (invalid transforms: {df_invalidtransform_with_index})"
            )
            QMessageBox.warning(
                None,
                "Error: Invalid Transform",
                errMsg,
            )
            self.updateStatusbar(errMsg)
            self.disableMappingMapButtons()
            return
        # If the mapping is valid, display a success message
        successMsg = (
            "The mapping is valid! "
            "You can now save it and use it to map the source dataset."
        )
        QMessageBox.information(
            None,
            "Success",
            successMsg,
        )
        self.updateStatusbar(successMsg)
        self.mappingSaveButton.setEnabled(True)
        self.mapButton.setEnabled(False)

    def initMapping(self):
        """Initialize an empty column/CDEs mapping table."""
        infoMsg = (
            "The empty mapping table is being created. "
            "Please wait until the process is finished."
        )
        self.updateStatusbar(infoMsg)
        # Create a first empty mapping table
        self.matchedCdeCodes = None
        self.columnsCDEsMappingData = pd.DataFrame(columns=MAPPING_TABLE_COLUMNS)
        # Create a pandas model for the mapping table
        self.columnsCDEsMappingPandasModel = PandasTableModel(
            self.columnsCDEsMappingData
        )
        # Set the model of the table view to the pandas model
        self.mappingTableView.setModel(self.columnsCDEsMappingPandasModel)
        self.mappingTableView.setSelectionBehavior(self.mappingTableView.SelectRows)
        self.mappingTableView.setSelectionMode(self.mappingTableView.SingleSelection)
        self.mappingTableView.setEditTriggers(
            self.mappingTableView.NoEditTriggers
        )  # disable editing
        # Handle the mapping table view row selection changed signal
        self.mappingTableView.selectionModel().currentRowChanged.connect(
            self.initializeMappingEditForm
        )
        # Select the first row of the mapping table view at the beginning
        indexRow = 0
        self.mappingTableView.selectRow(indexRow)
        # Handle the combox box current index changed signal for the CDE code column
        self.cdeCode.currentIndexChanged.connect(self.updateMappingEditForm)
        # Show status message
        infoMsg = (
            "The mapping has been created. You can now edit, validate, and save it!"
        )
        self.updateStatusbar(infoMsg)

    def mappingMatch(self):
        """Initialize the column/CDEs mapping based on fuzzy word matching and character embedding methods."""
        matchingMethod = self.initMatchingMethod.currentText()
        infoMsg = (
            f"The mapping is being initialize using the {matchingMethod} method."
            "Please wait until the process is finished."
        )
        self.updateStatusbar(infoMsg)
        # Create a first mapping table based on fuzzy matching
        (
            self.columnsCDEsMappingData,
            self.matchedCdeCodes,
            self.inputDatasetColumnEmbeddings,
            self.targetCDEsEmbeddings,
        ) = match_columns_to_cdes(
            dataset=self.inputDataset,
            schema=self.targetCDEs,
            nb_kept_matches=10,
            matching_method=matchingMethod,
        )
        # Create a pandas model for the mapping table
        self.columnsCDEsMappingPandasModel = PandasTableModel(
            self.columnsCDEsMappingData
        )
        # Set the model of the table view to the pandas model
        self.mappingTableView.setModel(self.columnsCDEsMappingPandasModel)
        self.mappingTableView.setSelectionBehavior(self.mappingTableView.SelectRows)
        self.mappingTableView.setSelectionMode(self.mappingTableView.SingleSelection)
        self.mappingTableView.setEditTriggers(
            self.mappingTableView.NoEditTriggers
        )  # disable editing
        # Handle the mapping table view row selection changed signal
        self.mappingTableView.selectionModel().currentRowChanged.connect(
            self.initializeMappingEditForm
        )
        # Select the first row of the mapping table view at the beginning
        indexRow = 0
        self.mappingTableView.selectRow(indexRow)
        # Handle the combox box current index changed signal for the CDE code column
        self.cdeCode.currentIndexChanged.connect(self.updateMappingEditForm)
        # Show status message
        infoMsg = "The mapping has been created. You can now edit, check, and save it!"
        self.updateStatusbar(infoMsg)
        self.enableMappingButtons()
        if matchingMethod != "fuzzy":
            self.embeddingVizButton.setEnabled(True)
        else:
            self.embeddingVizButton.setEnabled(False)
        self.matchingVizButton.setEnabled(True)

    def selectOutputFilename(self):
        """Select the output filename."""
        self.outputFilename = QFileDialog.getSaveFileName(
            None, "Select the output filename", "", "CSV files (*.csv)"
        )
        if self.outputFilename[0] == "":
            errMsg = "Please select a valid output filename."
            QMessageBox.warning(
                None,
                "Error",
                errMsg,
            )
            self.updateStatusbar(errMsg)
            return False
        if not self.outputFilename[0].endswith(".csv"):
            self.outputFilename = self.outputFilename[0] + ".csv"
            successMsg = (
                "The output filename has been updated to: " + self.outputFilename + "."
            )
            QMessageBox.information(
                None,
                successMsg,
            )
            self.updateStatusbar(successMsg)
        return True

    def updateStatusbar(self, message):
        """Update the statusbar with the given message."""
        self.statusbar.showMessage(message)
        self.statusbar.repaint()

    def map(self):
        """Map the input dataset to the target CDEs."""
        select = self.selectOutputFilename()
        # Exit function if the output filename is not properly set
        if not select:
            return
        # Check if the input dataset and the mapping file are loaded
        if not os.path.exists(self.inputDatasetPathLabel.text()):
            warn_msg = "Please load the input dataset!"
            QMessageBox.warning(
                None,
                "Warning",
                warn_msg,
                QMessageBox.Ok,
            )
            self.updateStatusbar(warn_msg)
            return
        if not os.path.exists(self.mappingFilePathLabel.text()):
            warn_msg = "Please save the mapping file of load an existing one!"
            QMessageBox.warning(
                None,
                "Warning",
                warn_msg,
                QMessageBox.Ok,
            )
            self.updateStatusbar(warn_msg)
            return
        # Proceed with the mapping
        self.mapButton.setEnabled(False)
        self.updateStatusbar("Mapping in progress...")
        # Load the input dataset
        input_dataset = pd.read_csv(self.inputDatasetPathLabel.text())
        # Load the mapping file
        with open(self.mappingFilePathLabel.text(), "r") as f:
            mapping = json.load(f)
        # Map the input dataset to the target CDEs
        output_dataset = map_dataset(
            input_dataset, mapping, self.targetCDEs["code"].tolist()
        )
        # Save the output dataset
        output_dataset.to_csv(
            self.outputFilename[0],
            index=False,
        )
        # Show a message box to inform the user that the mapping has
        # been done successfully
        successMsg = (
            "The mapping has been done successfully and "
            "the output dataset has been saved to: " + self.outputFilename[0] + "."
        )
        QMessageBox.information(
            None,
            "Success",
            successMsg,
            QMessageBox.Ok,
        )
        self.updateStatusbar(successMsg)
        self.mapButton.setEnabled(True)
