"""Standalone script which starts the MIP Dataset Mapper UI application."""

import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from mip_dmp.qt5.components.dataset_mapper_window import (
    MIPDatasetMapperWindow,
)


class MIPDatasetMapperUI(QMainWindow):
    """Main UI class for the MIP Dataset Mapper UI application."""

    def __init__(self):
        super(MIPDatasetMapperUI, self).__init__()
        self.ui = MIPDatasetMapperWindow(self)


def main():
    """Main function that starts the application."""
    app = QApplication(sys.argv)
    window = MIPDatasetMapperUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
