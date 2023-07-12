from qtpy.QtWidgets import QMenuBar, QMenu, QAction


class Menubar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self._init_ui()

    def _init_ui(self):
        self.file_menu = QMenu("File", parent=self)
        self.open_action = QAction("Open", parent=self)
        self.file_menu.addAction(self.open_action)
        self.addMenu(self.file_menu)
