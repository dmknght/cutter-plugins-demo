"""
Playing with Cutter's python plugin
Cutter version: 2.0.3
Rizin backend version: 0.3.0
Qt5 version: 5.15.2
Compiled with Python and Python bindings and Shiboken2 5.15.2
"""

import cutter
import json

from PySide2.QtCore import QObject, SIGNAL, Qt
from PySide2.QtWidgets import QAction, QTreeView, QMenu, QApplication, QTableWidget
from PySide2.QtGui import QStandardItemModel, QStandardItem


class SectionHashesWidget(cutter.CutterDockWidget):
    def __init__(self, parent, action):
        super(SectionHashesWidget, self).__init__(parent, action)
        self.setObjectName("SectionHashes")
        self.setWindowTitle("Section Hashes")
        self.table = QTreeView()
        self.table_data = QStandardItemModel(0, 4)

        self.init_table()
        # QObject.connect(cutter.core(), SIGNAL("seekChanged(RVA)"), self.update_contents)

    def init_table(self):
        self.table.setModel(self.table_data)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_data.setHeaderData(0, Qt.Horizontal, "Name")
        self.table_data.setHeaderData(1, Qt.Horizontal, "Address")
        self.table_data.setHeaderData(2, Qt.Horizontal, "Size")
        self.table_data.setHeaderData(3, Qt.Horizontal, "Hash")
        self.setWidget(self.table)

    def contextMenuEvent(self, event):
        # Tutorial example https://codeloop.org/how-to-create-context-menu-in-pyqt5/
        menu = QMenu()
        menu.addAction("Copy name", self.__copy_name)
        menu.addAction("Copy hash", self.__copy_hash)
        menu.addAction("Copy address", self.__copy_address)
        menu.addAction("Copy size", self.__copy_size)
        # Add separator example https://stackoverflow.com/a/33939764
        menu.addSeparator()
        menu.addAction("Copy row (Json)", self.__copy_row)
        menu.exec_(self.mapToGlobal(event.pos()))

    def __copy_row(self):
        row_data = {
            "Name": "",
            "Address": "",
            "Size": "",
            "Hash": "",
        }

        for column_id, key in enumerate(row_data.keys()):
            row_data[key] = self.table.selectedIndexes()[column_id].data()
        self.__to_clipboard(str(row_data))

    def __copy_name(self):
        # Get value from QModelIndex https://srinikom.github.io/pyside-docs/PySide/QtCore/QModelIndex.html
        # 0 is column Name. We want the section's name so it is hard coded
        self.__to_clipboard(self.table.selectedIndexes()[0].data())

    def __copy_hash(self):
        # 3 is column Hash. We want the section's hash so it is hard coded
        self.__to_clipboard(self.table.selectedIndexes()[3].data())

    def __copy_address(self):
        # 1 is column Address. We want the section's address so it is hard coded
        self.__to_clipboard(self.table.selectedIndexes()[1].data())

    def __copy_size(self):
        # 2 is column size. We want the section's size so it is hard coded
        self.__to_clipboard(self.table.selectedIndexes()[2].data())

    def __to_clipboard(self, text):
        # Push value to clipboard https://stackoverflow.com/a/23119741
        clip_board = QApplication.clipboard()
        clip_board.setText(text, mode=clip_board.Clipboard)

    def update_contents(self):
        # Add table using example from https://pythonbasics.org/pyqt-table/
        section_hashes = json.loads(cutter.cmd("iSj md5").strip())
        row_count = 0
        for section_info in section_hashes:
            if "md5" in section_info.keys():
                self.table_data.setItem(row_count, 0, QStandardItem(section_info["name"]))
                # Hex formating for int https://stackoverflow.com/a/12638477
                self.table_data.setItem(row_count, 1, QStandardItem(f"{section_info['paddr']:#08x}"))
                self.table_data.setItem(row_count, 2, QStandardItem(str(hex(section_info["size"]))))
                self.table_data.setItem(row_count, 3, QStandardItem(section_info["md5"]))
                row_count += 1
        for i in range(4):
            self.table.resizeColumnToContents(i)


class SectionHashes(cutter.CutterPlugin):
    name = "Section Hashes"
    description = "A custom plugin to show section hashes in a widget"
    version = "1.0"
    author = "Nong Hoang Tu"

    def setupPlugin(self):
        pass

    def setupInterface(self, main):
        action = QAction("Section hashes", main)
        action.setCheckable(True)
        widget = SectionHashesWidget(main, action)
        main.addPluginDockWidget(widget, action)

    def terminate(self):
        pass


def create_cutter_plugin():
    return SectionHashes()
