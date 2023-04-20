"""Class for the main window of the MIP Dataset Mapper UI application."""

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
)
import pkg_resources

from mip_dmp.dataset.mapping import initialize_mapping_table, map_dataset
from mip_dmp.qt5.model.table_model import (
    # NoEditorDelegate,
    PandasTableModel,
)


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
        "mappingSourceDatasetColumnDelegate",
        "mappingTargetCDECodeColumnDelegate",
        "mappingTargetCDETypeColumnDelegate",
        "mappingTransformTypeColumnDelegate",
        "mappingTransformColumnDelegate",
        "outputDirectoryPath",
        "outputFilename",
        "statusbar",
        "toolBar",
    ]

    def __init__(self, mainWindow):
        """Initialize the main window of the MIP Dataset Mapper UI application."""
        if not mainWindow.objectName():
            mainWindow.setObjectName(f"{WINDOW_NAME}")
        mainWindow.resize(1024, 768)
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
        self.mappingSaveButton.setEnabled(False)
        self.mapButton.setEnabled(False)

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
        targetCDEsToolLabel = QLabel("2. Target CDEs Metadata Schema:")
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
        # Add the load / save mapping file buttons to the tool bar
        mappingToolLabel = QLabel("3. Mapping file:")
        mappingToolLabel.setStyleSheet("QLabel { font-weight: bold; color: #222222;}")
        self.toolBar.addWidget(mappingToolLabel)
        self.toolBar.addAction(self.mappingCheckButton)
        self.toolBar.addAction(self.mappingSaveButton)
        self.toolBar.addAction(self.mappingLoadButton)
        # Add a spacer to the tool bar
        spacer3 = QWidget()
        spacer3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(spacer3)
        # Add a separator to the tool bar
        self.toolBar.addSeparator()
        # Add the map button to the tool bar
        actionsLabel = QLabel("4. Map:")
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
        # Set the mapping table
        self.mappingTableView = QTableView(self.columnsCDEsMappingGroupBox)
        self.mappingTableView.setGeometry(QRect(10, 70, 371, 231))
        # # Create group box for entering a new entry to the mapping table
        # self.newMappingGroupBox = QGroupBox()
        # # Set the layout of the new entry group box
        # self.newMappingGroupBoxLayout = QGridLayout()
        # # Create a widget to hold combo boxes for column and CDE
        # self.newMappingFormLayoutWidget = QWidget(self.newMappingGroupBox)
        # self.newMappingFormLayoutWidget.setGeometry(QRect(10, 30, 371, 31))
        # # Create the form layout for the combo boxes
        # self.newMappingFormLayout = QFormLayout(self.newMappingFormLayoutWidget)
        # self.newMappingFormLayout.setContentsMargins(0, 0, 0, 0)
        # # Create the combo boxe for column
        # self.newMappingColumnComboBox = QComboBox(self.newMappingFormLayoutWidget)
        # # Create the combo box for CDE
        # self.newMappingCDEComboBox = QComboBox(self.newMappingFormLayoutWidget)
        # # Create the add button
        # self.newMappingAddButton = QPushButton(self.newMappingGroupBox)
        # self.newMappingAddButton.setGeometry(QRect(300, 70, 81, 31))
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
        # self.mappingSaveButton.setGeometry(QRect(300, 310, 81, 31))
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
        # self.inputDatasetFormLayout.setWidget(
        #     0, QFormLayout.LabelRole, self.inputDatasetLoadButton
        # )
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
        # self.targetCDEsFormLayout.setWidget(
        #     0, QFormLayout.LabelRole, self.targetCDEsLoadButton
        # )
        self.targetCDEsFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.targetCDEsPathLabel
        )
        self.targetCDEsGroupBoxLayout.addWidget(
            self.targetCDEsFormLayoutWidget, 1, 0, 1, 1
        )
        self.leftCentralWidgetSplitter.addWidget(self.targetCDEsGroupBox)
        # Handle the widgets of the columns CDEs mapping group box (top right)
        self.columnsCDEsMappingGroupBox.setLayout(self.columnsCDEsMappingGroupBoxLayout)

        self.mappingFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.mappingFilePathLabel
        )
        self.columnsCDEsMappingGroupBoxLayout.addWidget(
            self.columnsCDEsMappingSplitter, 0, 0, 1, 1
        )
        self.columnsCDEsMappingSplitter.addWidget(self.mappingTableView)
        self.columnsCDEsMappingGroupBoxLayout.addWidget(
            self.mappingFormLayoutWidget, 1, 0, 1, 1
        )

        self.rightCentralWidgetSplitter.addWidget(self.columnsCDEsMappingGroupBox)
        # # Create group box for entering a new entry to the mapping table
        # # Set the layout of the new entry group box
        # self.newMappingGroupBox.setLayout(self.newMappingGroupBoxLayout)
        # # Add the column combo boxe to the form layout
        # self.newMappingFormLayout.setWidget(
        #     0, QFormLayout.LabelRole, self.newMappingColumnComboBox
        # )
        # # Add the CDE combo box to the form layout
        # self.newMappingFormLayout.setWidget(
        #     0, QFormLayout.FieldRole, self.newMappingCDEComboBox
        # )
        # # Add the form layout widget to the group box layout
        # self.newMappingGroupBoxLayout.addWidget(
        #     self.newMappingFormLayoutWidget, 0, 0, 1, 1
        # )
        # # Add the add button to the group box layout
        # self.newMappingGroupBoxLayout.addWidget(self.newMappingAddButton, 1, 0, 1, 1)
        # # Add the new entry group box to the tableview/new entry group splitter
        # self.columnsCDEsMappingSplitter.addWidget(self.newMappingGroupBox)
        # Handle the widgets of the output group box (bottom right)
        # self.outputGroupBox.setLayout(self.outputGroupBoxLayout)
        # self.outputFormLayout.setWidget(
        #     2, QFormLayout.LabelRole, self.outputFilenameLabel
        # )
        # self.outputFormLayout.setWidget(
        #     2, QFormLayout.FieldRole, self.outputFilenameSelectButton
        # )
        # self.outputGroupBoxLayout.addWidget(self.outputFormLayoutWidget, 1, 0, 1, 1)
        # # self.outputGroupBoxLayout.addWidget(self.mapButton, 3, 0, 1, 1)
        # self.rightCentralWidgetSplitter.addWidget(self.outputGroupBox)

    def connectButtons(self):
        """Connect the buttons to their corresponding functions."""
        self.inputDatasetLoadButton.triggered.connect(self.loadInputDataset)
        self.targetCDEsLoadButton.triggered.connect(self.loadCDEsFile)
        self.mappingLoadButton.triggered.connect(self.loadMapping)
        self.mappingCheckButton.triggered.connect(self.checkMapping)
        self.mappingSaveButton.triggered.connect(self.saveMapping)
        self.mapButton.triggered.connect(self.map)

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
            err_msg = (
                f"The input dataset file {self.inputDatasetPath[0]} does not exist. "
                "Please select a valid file!"
            )
            QMessageBox.warning(
                None,
                "Error",
                err_msg,
            )
            self.updateStatusbar(err_msg)
            self.disableSaveMappingAndMapButtons()
        else:
            self.inputDataset = pd.read_csv(self.inputDatasetPath[0])
            self.inputDatasetColumns = self.inputDataset.columns.tolist()
            self.inputDatasetPandasModel = PandasTableModel(self.inputDataset)
            self.inputDatasetTableView.setModel(self.inputDatasetPandasModel)
            self.updateStatusbar(f"Loaded input dataset {self.inputDatasetPath[0]}")
            if hasattr(self, "targetCDEsPath") and os.path.exists(
                self.targetCDEsPath[0]
            ):
                self.updateColumnCDEsMapping()
            self.disableSaveMappingAndMapButtons()

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
            err_msg = (
                f"The CDEs file {self.targetCDEsPath[0]} does not exist. "
                "Please select a valid file!"
            )
            QMessageBox.warning(
                None,
                "Error",
                err_msg,
            )
            self.updateStatusbar(err_msg)
            self.disableSaveMappingAndMapButtons()
        else:
            self.targetCDEs = pd.read_excel(self.targetCDEsPath[0])
            self.targetCDEsPandasModel = PandasTableModel(self.targetCDEs)
            self.targetCDEsTableView.setModel(self.targetCDEsPandasModel)
            success_msg = f"Loaded CDEs file {self.targetCDEsPath[0]}"
            self.updateStatusbar(success_msg)
            if hasattr(self, "inputDatasetPath") and os.path.exists(
                self.inputDatasetPath[0]
            ):
                self.updateColumnCDEsMapping()
            self.disableSaveMappingAndMapButtons()

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
            err_msg = (
                f"The mapping file {self.mappingFilePath[0]} does not exist. "
                "Please select a valid file!"
            )
            QMessageBox.warning(
                None,
                "Error",
                err_msg,
            )
            self.updateStatusbar(err_msg)
            self.disableSaveMappingAndMapButtons()
        else:
            success_msg = (
                f"Loaded mapping file {self.mappingFilePath[0]}. "
                "Please check the mapping and click on the Map button to map the input dataset."
            )
            self.updateStatusbar(success_msg)
            self.disableSaveMappingAndMapButtons()

    def saveMapping(self):
        """Save the mapping file."""
        self.mappingFilePath = QFileDialog.getSaveFileName(
            None, "Select the mapping file", "", "JSON files (*.json)"
        )
        path = Path(self.mappingFilePath[0])
        if path.suffix != ".json":
            err_msg = (
                f"The mapping file {self.mappingFilePath[0]} does not have a .json extension. "
                "Please select a valid file!"
            )
            QMessageBox.warning(
                None,
                "Error",
                err_msg,
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
        success_msg = f"Mapping saved to {self.mappingFilePath[0]}!"
        self.updateStatusbar(success_msg)
        self.mapButton.setEnabled(True)

    def disableSaveMappingAndMapButtons(self):
        """Disable the save mapping and map buttons."""
        self.mappingSaveButton.setEnabled(False)
        self.mapButton.setEnabled(False)

    def checkMapping(self):
        """Check the mapping."""
        # Check if the mapping contains unique column / CDE pairs
        if (
            len(self.columnsCDEsMappingData["cde_code"].unique())
            != len(self.columnsCDEsMappingData["cde_code"])
        ) or (
            len(self.columnsCDEsMappingData["dataset_column"].unique())
            != len(self.columnsCDEsMappingData["dataset_column"])
        ):
            err_msg = (
                "The mapping is not valid. "
                "Please check it and remove any mapping row "
                "that might re-map a CDE code or a column of "
                "the source dataset!"
            )
            QMessageBox.warning(
                None,
                "Error: Duplicate Column / CDEs Pairs",
                err_msg,
            )
            self.updateStatusbar(err_msg)
            self.disableSaveMappingAndMapButtons()
            return
        # Check if the mapping contains only valid CDE codes
        if self.columnsCDEsMappingData[
            self.columnsCDEsMappingData["cde_code"].isin(self.targetCDEs["code"])
        ].empty:
            err_msg = (
                "The mapping is not valid. "
                "Please check it and remove any invalid CDE code!"
            )
            QMessageBox.warning(
                None,
                "Error: Invalid CDE Codes",
                err_msg,
            )
            self.updateStatusbar(err_msg)
            self.disableSaveMappingAndMapButtons()
            return
        # Check if the mapping transform is correctly formatted
        transform_list = self.columnsCDEsMappingData["transform"].tolist()

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
                ast.literal_eval(f'"{transform}"')
                return False
            except ValueError:
                return True

        is_invalid_transform = list(map(is_invalid_map_transform, transform_list))
        if any(is_invalid_transform):
            df_invalidtransform_with_index = pd.DataFrame(
                {
                    "transform": [
                        transform_list[i]
                        for i in range(len(transform_list))
                        if is_invalid_transform[i]
                    ],
                    "mapping_row": [
                        i + 1
                        for i in range(len(transform_list))
                        if is_invalid_transform[i]
                    ],
                }
            )
            err_msg = (
                "The mapping is not valid. "
                "Please check it and correct "
                "any invalid transform!"
                f" (invalid transforms: {df_invalidtransform_with_index})"
            )
            QMessageBox.warning(
                None,
                "Error: Invalid Transform",
                err_msg,
            )
            self.updateStatusbar(err_msg)
            self.disableSaveMappingAndMapButtons()
            return
        # If the mapping is valid, display a success message
        success_msg = (
            "The mapping is valid! "
            "You can now save it and use it to map the source dataset."
        )
        QMessageBox.information(
            None,
            "Success",
            success_msg,
        )
        self.updateStatusbar(success_msg)
        self.mappingSaveButton.setEnabled(True)
        self.mapButton.setEnabled(False)

    def updateColumnCDEsMapping(self):
        """Update the column/CDEs mapping."""
        info_msg = (
            "The mapping is being created / updated. "
            "Please wait until the process is finished."
        )
        self.updateStatusbar(info_msg)
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
        # Set a custom delegates for the columns of the mapping table
        # self.mappingSourceDatasetColumnDelegate = NoEditorDelegate(
        #     self.mappingTableView
        # )
        # self.mappingTableView.setItemDelegateForColumn(
        #     0, self.mappingSourceDatasetColumnDelegate
        # )
        for index, row in self.columnsCDEsMappingData.iterrows():
            c = QComboBox()
            c.addItems(
                fuzzy_matched_cde_codes[row["cde_code"]][0]
            )  # first tuple element is the list of CDE codes
            i = self.mappingTableView.model().index(index, 1)
            self.mappingTableView.setIndexWidget(i, c)

        # self.mappingTargetCDECodeColumnDelegate = QComboBoxDelegate(
        #     self.mappingTableView
        # )
        # self.mappingTargetCDECodeColumnDelegate.setItems(
        #     self.targetCDEs["code"].tolist()
        # )
        # self.mappingTableView.setItemDelegateForColumn(
        #     1, self.mappingTargetCDECodeColumnDelegate
        # )
        # "mappingTargetCDECodeColumnDelegate"
        # "mappingTargetCDETypeColumnDelegate"
        # "mappingTransformTypeColumnDelegate"
        # "mappingTransformColumnDelegate"
        info_msg = (
            "The mapping has been created. You can now edit, validate, and save it!"
        )
        self.updateStatusbar(info_msg)

    def selectOutputFilename(self):
        """Select the output filename."""
        self.outputFilename = QFileDialog.getSaveFileName(
            None, "Select the output filename", "", "CSV files (*.csv)"
        )
        if self.outputFilename[0] == "":
            err_msg = "Please select a valid output filename."
            QMessageBox.warning(
                None,
                "Error",
                err_msg,
            )
            self.updateStatusbar(err_msg)
            return False
        if not self.outputFilename[0].endswith(".csv"):
            self.outputFilename = self.outputFilename[0] + ".csv"
            success_msg = (
                "The output filename has been updated to: " + self.outputFilename + "."
            )
            QMessageBox.information(
                None,
                success_msg,
            )
            self.updateStatusbar(success_msg)
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
        output_dataset = map_dataset(input_dataset, mapping)
        # Save the output dataset
        output_dataset.to_csv(
            self.outputFilename[0],
            index=False,
        )
        # Show a message box to inform the user that the mapping has
        # been done successfully
        success_msg = (
            "The mapping has been done successfully and "
            "the output dataset has been saved to: " + self.outputFilename[0] + "."
        )
        QMessageBox.information(
            None,
            "Success",
            success_msg,
            QMessageBox.Ok,
        )
        self.updateStatusbar(success_msg)
        self.mapButton.setEnabled(True)
