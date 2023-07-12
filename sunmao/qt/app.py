import sys
import typing as T

from qtpy import QtWidgets
from easynode.node_editor import NodeEditor
from easynode.setting import EditorSetting

from .ui.menubar import Menubar


class SunmaoQt(QtWidgets.QWidget):
    current_instance = None

    def __init__(self, editor_setting: T.Optional[EditorSetting] = None):
        super().__init__()
        self._editor_setting = editor_setting
        self.__class__.current_instance = self
        self._init_ui()

    def _init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.menubar = Menubar(parent=self)
        self.node_editor = NodeEditor(
            parent=self, setting=self._editor_setting)

        self.layout.setMenuBar(self.menubar)
        self.layout.addWidget(self.node_editor)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    instance = SunmaoQt()
    instance.show()
    app.exec_()
