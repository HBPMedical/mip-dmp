"""Module to describe Qt Table Models."""

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QItemDelegate, QLineEdit, QComboBox


class PandasTableModel(QtCore.QAbstractTableModel):
    """Qt Table Model for Pandas DataFrames."""

    def __init__(self, data):
        """Initialize the table model.

        Parameters
        ----------
        data : pandas.DataFrame
            Data to be displayed in the table.
        """
        super(PandasTableModel, self).__init__()
        self._data = data

    def setData(self, data):
        self._data = data
        self.layoutChanged.emit()

    def data(self, index, role):
        """Return the data for the given index and role."""
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        """Return the number of rows in the table."""
        return self._data.shape[0]

    def columnCount(self, index):
        """Return the number of columns in the table."""
        return self._data.shape[1]

    def flags(self, index):
        """Return the flags for the given index."""
        if not index.isValid():
            return Qt.ItemIsEnabled
        return (
            super().flags(index) | Qt.ItemIsEditable | Qt.ItemIsSelectable
        )  # add editable and selectable flag.

    def headerData(self, section, orientation, role):
        """Return the header data for the given section."""
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def setData(self, index, value, role):
        """Set the data for the given index and role."""
        if role == Qt.EditRole:
            # Set the value into the frame.
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False


class QComboBoxDelegate(QItemDelegate):
    """Class to define a custom item delegate with QComboBox editor."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def setItems(self, items):
        self.items[:] = items

    def createEditor(self, parent, opt, index):
        comboBox = QComboBox(parent)
        comboBox.addItems(self.items)
        comboBox.setCurrentIndex(1)
        comboBox.currentTextChanged.connect(lambda: self.commitData.emit(comboBox))
        return comboBox

    # def setEditorData(self, editor, index):
    #     """Set the editor data for the given index."""
    #     value = index.model().data(index, Qt.EditRole)
    #     editor.setCurrentIndex(value)

    # def setModelData(self, editor, model, index):
    #     """Set the model data for the given index."""
    #     value = editor.currentIndex()
    #     model.setData(index, value, Qt.EditRole)

    # def updateEditorGeometry(self, editor, option, index):
    #     """Update the editor geometry for the given index."""
    #     editor.setGeometry(option.rect)


class NoEditorDelegate(QItemDelegate):
    """Class to define a custom item delegate with no editor."""

    def createEditor(self, parent, opt, index):
        """Create the editor for the given index."""
        return None

    # def setEditorData(self, editor, index):
    #     """Set the editor data for the given index."""
    #     value = index.model().data(index, Qt.EditRole)
    #     editor.setText(value)

    # def setModelData(self, editor, model, index):
    #     """Set the model data for the given index."""
    #     value = editor.text()
    #     model.setData(index, value, Qt.EditRole)

    # def updateEditorGeometry(self, editor, option, index):
    #     """Update the editor geometry for the given index."""
    #     editor.setGeometry(option.rect)
