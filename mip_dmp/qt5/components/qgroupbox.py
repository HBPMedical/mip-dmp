from PySide2.QtWidgets import (
    QGroupBox,
    QGridLayout,
    QTableView,
    QAbstractItemView,
    QWidget,
    QFormLayout,
    QPushButton,
    QLabel,
)
from mip_dmp.qt5.components.dataset_mapper_window import MIPDatasetMapperWindow


def create_input_dataset_qgroupbox(window: MIPDatasetMapperWindow):
    """Add the input dataset QGroupBox and underlied compnents to the main window"""
    window.inputDatasetGroupBox = QGroupBox(window.centralwidget)
    window.inputDatasetGroupBox.setObjectName("inputDatasetGroupBox")
    # Set the layout of the group box
    window.inputDatasetGroupBoxLayout = QGridLayout()
    window.inputDatasetGroupBoxLayout.setObjectName("inputDatasetGroupBoxLayout")
    window.inputDatasetGroupBox.setLayout(window.inputDatasetGroupBoxLayout)
    # Set the table view
    window.inputDatasetTableView = QTableView(window.inputDatasetGroupBox)
    window.inputDatasetTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    window.inputDatasetTableView.setObjectName("inputDatasetTableView")
    window.inputDatasetTableView.setGeometry(QRect(10, 71, 341, 281))
    # Add the table view to the group box layout
    window.inputDatasetGroupBoxLayout.addWidget(
        window.inputDatasetTableView, 1, 0, 1, 1
    )
    # Set the form layout with button to load the dataset
    window.inputDatasetFormLayoutWidget = QWidget(window.inputDatasetGroupBox)
    window.inputDatasetFormLayoutWidget.setObjectName("inputDatasetFormLayoutWidget")
    window.inputDatasetFormLayoutWidget.setGeometry(QRect(10, 30, 341, 31))
    window.inputDatasetFormLayout = QFormLayout(window.inputDatasetFormLayoutWidget)
    window.inputDatasetFormLayout.setObjectName("inputDatasetFormLayout")
    window.inputDatasetFormLayout.setContentsMargins(0, 0, 0, 0)
    window.inputDatasetLoadButton = QPushButton(window.inputDatasetFormLayoutWidget)
    window.inputDatasetLoadButton.setObjectName("inputDatasetLoadButton")
    window.inputDatasetFormLayout.setWidget(
        0, QFormLayout.LabelRole, window.inputDatasetLoadButton
    )
    window.inputDatasetPathLabel = QLabel(window.inputDatasetFormLayoutWidget)
    window.inputDatasetPathLabel.setObjectName("inputDatasetPathLabel")
    window.inputDatasetFormLayout.setWidget(
        0, QFormLayout.FieldRole, window.inputDatasetPathLabel
    )
    # Add the form layout widget to the group box layout
    window.inputDatasetGroupBoxLayout.addWidget(
        window.inputDatasetFormLayoutWidget, 0, 0, 1, 1
    )

    return window
