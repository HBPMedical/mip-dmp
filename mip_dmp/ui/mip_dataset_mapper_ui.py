"""Standalone script which starts the MIP Dataset Mapper UI application."""

import sys
from os import path as op
from pkg_resources import resource_filename
from PySide2 import QtGui
from PySide2.QtWidgets import QApplication, QMainWindow
from mip_dmp.qt5.components.dataset_mapper_window import (
    MIPDatasetMapperWindow,
)


class MIPDatasetMapperUI(QMainWindow):
    """Main UI class for the MIP Dataset Mapper UI application."""

    def __init__(self):
        super(MIPDatasetMapperUI, self).__init__()
        self.setIcon()
        self.ui = MIPDatasetMapperWindow(self)

    def setIcon(self):
        """Set the application icon."""
        appIcon = QtGui.QIcon(
            resource_filename("mip_dmp", op.join("qt5", "assets", "mip_dmp_icon.png"))
        )
        self.setWindowIcon(appIcon)


def main():
    """Main function that starts the application."""
    app = QApplication(sys.argv)
    window = MIPDatasetMapperUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
