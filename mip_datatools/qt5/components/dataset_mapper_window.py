"""Class for the main window of the MIP Dataset Mapper UI application."""

import os
import json
from pathlib import Path
import pandas as pd
from PySide2.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PySide2.QtWidgets import (
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
)
import pkg_resources

from mip_datatools.dataset.mapping import initialize_mapping_table, map_dataset
from mip_datatools.qt5.model.qt_table_model import PandasTableModel


WINDOW_NAME = "MIPDatasetMapperUI"


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
        "statusbar",
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
        "outputDirectoryPath",
        "outputFilename",
    ]

    def __init__(self):
        """Initialize the main window of the MIP Dataset Mapper UI application."""
        pass

    def setupUi(self, mainWindow):
        """Setup the main window of the MIP Dataset Mapper UI application.

        Parameters
        ----------
        mainWindow : QMainWindow
            Main window of the MIP Dataset Mapper UI application.
        """
        if not mainWindow.objectName():
            mainWindow.setObjectName(f"{WINDOW_NAME}")
        mainWindow.resize(800, 600)
        styleSheetFile = pkg_resources.resource_filename(
            "mip_datatools", os.path.join("qt5", "assets", "stylesheet.qss")
        )
        with open(styleSheetFile, "r") as fh:
            mainWindow.setStyleSheet(fh.read())
        #######################################################################
        # Set the central widget
        #######################################################################
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralWidgetGridLayout = QGridLayout(self.centralwidget)
        self.centralWidgetGridLayout.setObjectName("centralWidgetGridLayout")
        #######################################################################
        # Set the different main splitters
        #######################################################################
        # Set the main horizontal splitter
        self.centralWidgetSplitter = QSplitter(Qt.Horizontal)
        self.centralWidgetSplitter.setObjectName("centralWidgetSplitter")
        self.centralWidgetGridLayout.addWidget(self.centralWidgetSplitter, 0, 0, 1, 1)
        # Set the left side of the splitter
        self.leftCentralWidgetSplitter = QSplitter(Qt.Vertical)
        self.leftCentralWidgetSplitter.setObjectName("leftSplitter")
        self.centralWidgetSplitter.addWidget(self.leftCentralWidgetSplitter)
        # Set the right side of the splitter
        self.rightCentralWidgetSplitter = QSplitter(Qt.Vertical)
        self.rightCentralWidgetSplitter.setObjectName("rightSplitter")
        self.centralWidgetSplitter.addWidget(self.rightCentralWidgetSplitter)
        #######################################################################
        # Set the input dataset group box (top left)
        #######################################################################
        self.inputDatasetGroupBox = QGroupBox(self.centralwidget)
        self.inputDatasetGroupBox.setObjectName("inputDatasetGroupBox")
        # Set the layout of the group box
        self.inputDatasetGroupBoxLayout = QGridLayout()
        self.inputDatasetGroupBoxLayout.setObjectName("inputDatasetGroupBoxLayout")
        self.inputDatasetGroupBox.setLayout(self.inputDatasetGroupBoxLayout)
        # Set the table view
        self.inputDatasetTableView = QTableView(self.inputDatasetGroupBox)
        self.inputDatasetTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.inputDatasetTableView.setObjectName("inputDatasetTableView")
        self.inputDatasetTableView.setGeometry(QRect(10, 71, 341, 281))
        # Add the table view to the group box layout
        self.inputDatasetGroupBoxLayout.addWidget(
            self.inputDatasetTableView, 1, 0, 1, 1
        )
        # Set the form layout with button to load the dataset
        self.inputDatasetFormLayoutWidget = QWidget(self.inputDatasetGroupBox)
        self.inputDatasetFormLayoutWidget.setObjectName("inputDatasetFormLayoutWidget")
        self.inputDatasetFormLayoutWidget.setGeometry(QRect(10, 30, 341, 31))
        self.inputDatasetFormLayout = QFormLayout(self.inputDatasetFormLayoutWidget)
        self.inputDatasetFormLayout.setObjectName("inputDatasetFormLayout")
        self.inputDatasetFormLayout.setContentsMargins(0, 0, 0, 0)
        self.inputDatasetLoadButton = QPushButton(self.inputDatasetFormLayoutWidget)
        self.inputDatasetLoadButton.setObjectName("inputDatasetLoadButton")
        self.inputDatasetFormLayout.setWidget(
            0, QFormLayout.LabelRole, self.inputDatasetLoadButton
        )
        self.inputDatasetPathLabel = QLabel(self.inputDatasetFormLayoutWidget)
        self.inputDatasetPathLabel.setObjectName("inputDatasetPathLabel")
        self.inputDatasetFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.inputDatasetPathLabel
        )
        # Add the form layout widget to the group box layout
        self.inputDatasetGroupBoxLayout.addWidget(
            self.inputDatasetFormLayoutWidget, 0, 0, 1, 1
        )
        # Add the group box to the left splitter
        self.leftCentralWidgetSplitter.addWidget(self.inputDatasetGroupBox)
        #######################################################################
        # Set the target CDEs group box (bottom left)
        #######################################################################
        self.targetCDEsGroupBox = QGroupBox(self.centralwidget)
        self.targetCDEsGroupBox.setObjectName("targetCDEsGroupBox")
        # Set the layout of the group box
        self.targetCDEsGroupBoxLayout = QGridLayout()
        self.targetCDEsGroupBoxLayout.setObjectName("targetCDEsGroupBoxLayout")
        # Set layout of the group box
        self.targetCDEsGroupBox.setLayout(self.targetCDEsGroupBoxLayout)
        # Set the table view
        self.targetCDEsTableView = QTableView(self.targetCDEsGroupBox)
        self.targetCDEsTableView.setObjectName("targetCDEsTableView")
        self.targetCDEsTableView.setGeometry(QRect(10, 70, 341, 101))
        self.targetCDEsTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Add the table view to the group box layout
        self.targetCDEsGroupBoxLayout.addWidget(self.targetCDEsTableView, 1, 0, 1, 1)
        # Set the form layout with button to load the CDEs file
        self.targetCDEsFormLayoutWidget = QWidget(self.targetCDEsGroupBox)
        self.targetCDEsFormLayoutWidget.setObjectName("targetCDEsFormLayoutWidget")
        self.targetCDEsFormLayoutWidget.setGeometry(QRect(10, 30, 341, 31))
        self.targetCDEsFormLayout = QFormLayout(self.targetCDEsFormLayoutWidget)
        self.targetCDEsFormLayout.setObjectName("targetCDEsFormLayout")
        self.targetCDEsFormLayout.setContentsMargins(0, 0, 0, 0)
        self.targetCDEsLoadButton = QPushButton(self.targetCDEsFormLayoutWidget)
        self.targetCDEsLoadButton.setObjectName("targetCDEsLoadButton")
        self.targetCDEsFormLayout.setWidget(
            0, QFormLayout.LabelRole, self.targetCDEsLoadButton
        )
        self.targetCDEsPathLabel = QLabel(self.targetCDEsFormLayoutWidget)
        self.targetCDEsPathLabel.setObjectName("targetCDEsPathLabel")
        self.targetCDEsFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.targetCDEsPathLabel
        )
        # Add the form layout widget to the group box layout
        self.targetCDEsGroupBoxLayout.addWidget(
            self.targetCDEsFormLayoutWidget, 0, 0, 1, 1
        )
        # Add the group box to the left splitter
        self.leftCentralWidgetSplitter.addWidget(self.targetCDEsGroupBox)
        #######################################################################
        # Set the columns CDEs mapping group box (top right)
        #######################################################################
        self.columnsCDEsMappingGroupBox = QGroupBox(self.centralwidget)
        self.columnsCDEsMappingGroupBox.setObjectName("columnsCDEsMappingGroupBox")
        # Set the layout of the group box
        self.columnsCDEsMappingGroupBoxLayout = QGridLayout()
        self.columnsCDEsMappingGroupBoxLayout.setObjectName(
            "columnsCDEsMappingGroupBoxLayout"
        )
        # Set layout of the group box
        self.columnsCDEsMappingGroupBox.setLayout(self.columnsCDEsMappingGroupBoxLayout)
        # Set the form to load the mapping file
        self.mappingFormLayoutWidget = QWidget(self.columnsCDEsMappingGroupBox)
        self.mappingFormLayoutWidget.setObjectName("mappingFormLayoutWidget")
        self.mappingFormLayoutWidget.setGeometry(QRect(10, 30, 371, 31))
        self.mappingFormLayout = QFormLayout(self.mappingFormLayoutWidget)
        self.mappingFormLayout.setObjectName("mappingFormLayout")
        self.mappingFormLayout.setContentsMargins(0, 0, 0, 0)
        self.mappingLoadButton = QPushButton(self.mappingFormLayoutWidget)
        self.mappingLoadButton.setObjectName("mappingLoadButton")
        self.mappingFormLayout.setWidget(
            0, QFormLayout.LabelRole, self.mappingLoadButton
        )
        self.mappingFilePathLabel = QLabel(self.mappingFormLayoutWidget)
        self.mappingFilePathLabel.setObjectName("mappingFilePathLabel")
        self.mappingFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.mappingFilePathLabel
        )
        # Add the form layout widget to the group box layout
        self.columnsCDEsMappingGroupBoxLayout.addWidget(
            self.mappingFormLayoutWidget, 0, 0, 1, 1
        )
        # Set the splitter for the mapping table and the new entry form
        self.columnsCDEsMappingSplitter = QSplitter(Qt.Vertical)
        self.columnsCDEsMappingSplitter.setObjectName("columnsCDEsMappingSplitter")
        self.columnsCDEsMappingGroupBoxLayout.addWidget(
            self.columnsCDEsMappingSplitter, 1, 0, 1, 1
        )
        # Set the mapping table
        self.mappingTableView = QTableView(self.columnsCDEsMappingGroupBox)
        self.mappingTableView.setObjectName("mappingTableView")
        self.mappingTableView.setGeometry(QRect(10, 70, 371, 231))
        self.columnsCDEsMappingSplitter.addWidget(self.mappingTableView)

        # # Create group box for entering a new entry to the mapping table
        # self.newMappingGroupBox = QGroupBox()
        # self.newMappingGroupBox.setObjectName("newMappingGroupBox")
        # # Set the layout of the new entry group box
        # self.newMappingGroupBoxLayout = QGridLayout()
        # self.newMappingGroupBoxLayout.setObjectName("newMappingGroupBoxLayout")
        # self.newMappingGroupBox.setLayout(self.newMappingGroupBoxLayout)
        # # Create a widget to hold combo boxes for column and CDE
        # self.newMappingFormLayoutWidget = QWidget(self.newMappingGroupBox)
        # self.newMappingFormLayoutWidget.setObjectName("newMappingFormLayoutWidget")
        # self.newMappingFormLayoutWidget.setGeometry(QRect(10, 30, 371, 31))
        # # Create the form layout for the combo boxes
        # self.newMappingFormLayout = QFormLayout(self.newMappingFormLayoutWidget)
        # self.newMappingFormLayout.setObjectName("newMappingFormLayout")
        # self.newMappingFormLayout.setContentsMargins(0, 0, 0, 0)
        # # Create the combo boxe for column
        # self.newMappingColumnComboBox = QComboBox(self.newMappingFormLayoutWidget)
        # self.newMappingColumnComboBox.setObjectName("newMappingColumnComboBox")
        # # Add the column combo boxe to the form layout
        # self.newMappingFormLayout.setWidget(
        #     0, QFormLayout.LabelRole, self.newMappingColumnComboBox
        # )
        # # Create the combo box for CDE
        # self.newMappingCDEComboBox = QComboBox(self.newMappingFormLayoutWidget)
        # self.newMappingCDEComboBox.setObjectName("newMappingCDEComboBox")
        # # Add the CDE combo box to the form layout
        # self.newMappingFormLayout.setWidget(
        #     0, QFormLayout.FieldRole, self.newMappingCDEComboBox
        # )
        # # Add the form layout widget to the group box layout
        # self.newMappingGroupBoxLayout.addWidget(
        #     self.newMappingFormLayoutWidget, 0, 0, 1, 1
        # )
        # # Create the add button
        # self.newMappingAddButton = QPushButton(self.newMappingGroupBox)
        # self.newMappingAddButton.setObjectName("newMappingAddButton")
        # self.newMappingAddButton.setGeometry(QRect(300, 70, 81, 31))
        # # Add the add button to the group box layout
        # self.newMappingGroupBoxLayout.addWidget(self.newMappingAddButton, 1, 0, 1, 1)
        # # Add the new entry group box to the tableview/new entry group splitter
        # self.columnsCDEsMappingSplitter.addWidget(self.newMappingGroupBox)
        # Create the save button
        self.mappingSaveButton = QPushButton(self.columnsCDEsMappingGroupBox)
        self.mappingSaveButton.setObjectName("mappingSaveButton")
        self.mappingSaveButton.setGeometry(QRect(300, 310, 81, 31))
        # Add the save button to the group box layout
        self.columnsCDEsMappingGroupBoxLayout.addWidget(
            self.mappingSaveButton, 2, 0, 1, 1
        )
        # Add the mapping group box to the central widget
        self.rightCentralWidgetSplitter.addWidget(self.columnsCDEsMappingGroupBox)
        #######################################################################
        # Set the output group box (bottom right)
        #######################################################################
        self.outputGroupBox = QGroupBox(self.centralwidget)
        self.outputGroupBox.setObjectName("outputGroupBox")
        # Set the layout of the output group box
        self.outputGroupBoxLayout = QGridLayout()
        self.outputGroupBoxLayout.setObjectName("outputGroupBoxLayout")
        self.outputGroupBox.setLayout(self.outputGroupBoxLayout)
        # Create widget to hold the form layout for specifying the
        # output directory / filename
        self.outputFormLayoutWidget = QWidget(self.outputGroupBox)
        self.outputFormLayoutWidget.setObjectName("outputFormLayoutWidget")
        self.outputFormLayoutWidget.setGeometry(QRect(10, 40, 371, 71))
        # Create the form layout
        self.outputFormLayout = QFormLayout(self.outputFormLayoutWidget)
        self.outputFormLayout.setObjectName("outputFormLayout")
        self.outputFormLayout.setContentsMargins(0, 0, 0, 0)
        # Create the output directory label
        self.outputDirectoryLabel = QLabel(self.outputFormLayoutWidget)
        self.outputDirectoryLabel.setObjectName("outputDirectoryLabel")
        # Add the output directory label to the form layout
        self.outputFormLayout.setWidget(
            1, QFormLayout.LabelRole, self.outputDirectoryLabel
        )
        # Create the output directory select button
        self.outputDirectorySelectButton = QPushButton(self.outputFormLayoutWidget)
        self.outputDirectorySelectButton.setObjectName("outputDirectorySelectButton")
        # Add the output directory select button to the form layout
        self.outputFormLayout.setWidget(
            1, QFormLayout.FieldRole, self.outputDirectorySelectButton
        )
        # Create the output filename label
        self.outputFilenameLabel = QLabel(self.outputFormLayoutWidget)
        self.outputFilenameLabel.setObjectName("outputFilenameLabel")
        # Add the output filename label to the form layout
        self.outputFormLayout.setWidget(
            2, QFormLayout.LabelRole, self.outputFilenameLabel
        )
        # Create the output filename select button
        self.outputFilenameSelectButton = QPushButton(self.outputFormLayoutWidget)
        self.outputFilenameSelectButton.setObjectName("outputFilenameSelectButton")
        # Add the output filename select button to the form layout
        self.outputFormLayout.setWidget(
            2, QFormLayout.FieldRole, self.outputFilenameSelectButton
        )
        # Add the output form layout widget to the group box layout
        self.outputGroupBoxLayout.addWidget(self.outputFormLayoutWidget, 1, 0, 1, 1)
        # Create the map button
        self.mapButton = QPushButton(self.outputGroupBox)
        self.mapButton.setObjectName("mapButton")
        self.mapButton.setGeometry(QRect(300, 120, 80, 31))
        # Add the map button to the group box layout
        self.outputGroupBoxLayout.addWidget(self.mapButton, 3, 0, 1, 1)
        # Add the output group box to the right splitter of central widget
        self.rightCentralWidgetSplitter.addWidget(self.outputGroupBox)
        #######################################################################
        # Set the central widget
        #######################################################################
        mainWindow.setCentralWidget(self.centralwidget)
        #######################################################################
        # Set the status bar
        #######################################################################
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        #######################################################################
        # Set the text of the UI elements
        #######################################################################
        self.retranslateUi(mainWindow)
        #######################################################################
        # Add click listener functions to the Button elements
        #######################################################################
        self.connectButtons()
        #######################################################################
        # Search recursively for all child objects of the given object, and
        # connect matching signals from them to slots of object
        #######################################################################
        QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        """Set the text of the UI elements."""
        mainWindow.setWindowTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", f"{WINDOW_NAME}", None)
        )
        self.targetCDEsGroupBox.setTitle(
            QCoreApplication.translate(
                f"{WINDOW_NAME}", "Target CDEs Metadata Schema", None
            )
        )
        self.targetCDEsLoadButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Load", None)
        )
        self.targetCDEsPathLabel.setText(
            QCoreApplication.translate(
                f"{WINDOW_NAME}", "<Please load a CDEs file in .xlxs>", None
            )
        )
        self.outputGroupBox.setTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Output CSV Dataset", None)
        )
        self.mapButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Map", None)
        )
        self.outputDirectoryLabel.setText(
            QCoreApplication.translate(
                f"{WINDOW_NAME}", "Output Directory: <Please select a directory>", None
            )
        )
        self.outputDirectorySelectButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Select", None)
        )
        self.outputFilenameLabel.setText(
            QCoreApplication.translate(
                f"{WINDOW_NAME}", "Output filename: <Please enter the filename> ", None
            )
        )
        self.outputFilenameSelectButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Select", None)
        )
        self.inputDatasetGroupBox.setTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Input Dataset", None)
        )
        self.inputDatasetLoadButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Load", None)
        )
        self.inputDatasetPathLabel.setText(
            QCoreApplication.translate(
                f"{WINDOW_NAME}", "<Please load a CSV file...>", None
            )
        )
        self.columnsCDEsMappingGroupBox.setTitle(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Columns / CDEs Mapping", None)
        )
        self.mappingSaveButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Save as", None)
        )
        self.mappingLoadButton.setText(
            QCoreApplication.translate(f"{WINDOW_NAME}", "Load", None)
        )
        self.mappingFilePathLabel.setText(
            QCoreApplication.translate(
                f"{WINDOW_NAME}", "<Please load an existing mapping json file...>", None
            )
        )
        # self.newMappingCDEComboBox.setItemText(
        #     0, QCoreApplication.translate(f"{WINDOW_NAME}", "Select a CDE", None)
        # )
        # self.newMappingColumnComboBox.setItemText(
        #     0, QCoreApplication.translate(f"{WINDOW_NAME}", "Select a column", None)
        # )
        # self.newMappingAddButton.setText(
        #     QCoreApplication.translate(f"{WINDOW_NAME}", "Add", None)
        # )
        # self.newMappingGroupBox.setTitle(
        #     QCoreApplication.translate(f"{WINDOW_NAME}", "New Column/CDE Mapping", None)
        # )

    def connectButtons(self):
        """Connect the buttons to their corresponding functions."""
        self.inputDatasetLoadButton.clicked.connect(self.loadInputDataset)
        self.targetCDEsLoadButton.clicked.connect(self.loadCDEsFile)
        self.mappingLoadButton.clicked.connect(self.loadMapping)
        self.mappingSaveButton.clicked.connect(self.saveMapping)
        self.outputDirectorySelectButton.clicked.connect(self.selectOutputDirectory)
        self.outputFilenameSelectButton.clicked.connect(self.selectOutputFilename)
        self.mapButton.clicked.connect(self.map)

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
            QMessageBox.warning(
                None,
                "Error",
                "The input dataset file does not exist. Please select a valid file.",
            )
        else:
            self.inputDataset = pd.read_csv(self.inputDatasetPath[0])
            self.inputDatasetColumns = self.inputDataset.columns.tolist()
            self.inputDatasetPandasModel = PandasTableModel(self.inputDataset)
            self.inputDatasetTableView.setModel(self.inputDatasetPandasModel)
            if hasattr(self, "targetCDEsPath") and os.path.exists(
                self.targetCDEsPath[0]
            ):
                self.updateColumnCDEsMapping()

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
            QMessageBox.warning(
                None,
                "Error",
                "The CDEs file does not exist. Please select a valid file.",
            )
        else:
            self.targetCDEs = pd.read_excel(self.targetCDEsPath[0])
            self.targetCDEsPandasModel = PandasTableModel(self.targetCDEs)
            self.targetCDEsTableView.setModel(self.targetCDEsPandasModel)
            if hasattr(self, "inputDatasetPath") and os.path.exists(
                self.inputDatasetPath[0]
            ):
                self.updateColumnCDEsMapping()

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
            QMessageBox.warning(
                None,
                "Error",
                "The mapping file does not exist. Please select a valid file.",
            )

    def saveMapping(self):
        """Save the mapping file."""
        self.mappingFilePath = QFileDialog.getSaveFileName(
            None, "Select the mapping file", "", "JSON files (*.json)"
        )
        path = Path(self.mappingFilePath[0])
        if path.suffix != ".json":
            QMessageBox.warning(
                None,
                "Error",
                "The mapping file must be a .json file. Please enter a valid .json file extension.",
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

    def updateColumnCDEsMapping(self):
        """Update the column/CDEs mapping."""
        # Create a first mapping table based on fuzzy matching
        (
            self.columnsCDEsMappingData,
            fuzzy_matched_cde_codes,
        ) = initialize_mapping_table(dataset=self.inputDataset, schema=self.targetCDEs)
        # Create a pandas model for the mapping table
        self.columnsCDEsMappingPandasModel = PandasTableModel(
            self.columnsCDEsMappingData
        )
        # Set the model of the table view to the pandas model
        self.mappingTableView.setModel(self.columnsCDEsMappingPandasModel)

    def selectOutputDirectory(self):
        """Select the output directory."""
        self.outputDirectoryPath = QFileDialog.getExistingDirectory(
            None, "Select the output directory"
        )
        self.outputDirectoryLabel.setText(self.outputDirectoryPath)
        if not os.path.exists(self.outputDirectoryPath):
            QMessageBox.warning(
                None,
                "Error",
                "The output directory does not exist. Please select a valid directory.",
            )

    def selectOutputFilename(self):
        """Select the output filename."""
        self.outputFilename = QFileDialog.getSaveFileName(
            None, "Select the output filename", "", "CSV files (*.csv)"
        )
        self.outputFilenameLabel.setText(self.outputFilename[0])

    def map(self):
        """Map the input dataset to the target CDEs."""
        # Check if the input dataset, the CDEs file and the mapping file are loaded
        if not os.path.exists(self.inputDatasetPathLabel.text()):
            QMessageBox.warning(
                None,
                "Warning",
                "Please load the input dataset!",
                QMessageBox.Ok,
            )
            return

        if not os.path.exists(self.mappingFilePathLabel.text()):
            QMessageBox.warning(
                None,
                "Warning",
                "Please save the mapping file of load an existing one!",
                QMessageBox.Ok,
            )
            return

        # Proceed with the mapping
        self.mapButton.setText("Mapping...")
        self.mapButton.setEnabled(False)
        self.statusbar.showMessage("Mapping in progress...")
        self.statusbar.repaint()

        # Load the input dataset
        input_dataset = pd.read_csv(self.inputDatasetPathLabel.text())

        # Load the mapping file
        with open(self.mappingFilePathLabel.text(), "r") as f:
            mapping = json.load(f)

        # Map the input dataset to the target CDEs
        output_dataset = map_dataset(input_dataset, mapping)

        # Save the output dataset
        output_dataset.to_csv(
            os.path.join(self.outputDirectoryPath, self.outputFilename[0]),
            index=False,
        )

        self.mapButton.setText("Map")
        self.mapButton.setEnabled(True)
        self.statusbar.showMessage("Mapping Done!")
        self.statusbar.repaint()
