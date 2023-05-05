"""Standalone script which starts the MIP Dataset Mapper UI application."""

import sys
from os import path as op
from os import environ as env
from pkg_resources import resource_filename
from PySide2 import QtGui
from PySide2.QtWidgets import QApplication, QMainWindow

# Disable Tensorflow warnings, other options are:
# - 0 (default): all messages are logged (default behavior)
# - 1: INFO messages are not printed
# - 2: INFO and WARNING messages are not printed
# - 3: INFO, WARNING, and ERROR messages are not printed
# Note: this has to be done before importing tensorflow
# that is done for the first time when importing chars2vec
# in mip_dmp/io.py
env["TF_CPP_MIN_LOG_LEVEL"] = "3"  # noqa

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

    def closeEvent(self, event):
        """Close all windows."""
        self.ui.embeddingWidget.close()
        self.close()


def main():
    """Main function that starts the application."""
    app = QApplication(sys.argv)
    window = MIPDatasetMapperUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
