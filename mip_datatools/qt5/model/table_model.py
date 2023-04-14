"""Module to describe Qt Table Models."""

from PySide2 import QtCore
from PySide2.QtCore import Qt


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

        return super().flags(index) | Qt.ItemIsEditable  # add editable flag.

    def headerData(self, section, orientation, role):
        """Return the header data for the given section and orientation."""
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
            return True

        return False
