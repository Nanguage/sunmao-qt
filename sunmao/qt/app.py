import sys
import typing as T

from qtpy import QtWidgets
from easynode.node_editor import NodeEditor
from easynode.setting import EditorSetting
from sunmao.api import Session, Flow, compute

from .ui.menubar import Menubar


class SunmaoQt(QtWidgets.QWidget):
    current_instance = None

    def __init__(
            self,
            session: Session,
            editor_setting: T.Optional[EditorSetting] = None):
        super().__init__()
        self._editor_setting = editor_setting
        self.__class__.current_instance = self
        self._init_ui()
        self.session = session

    def _init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.menubar = Menubar(parent=self)
        self.node_editor = NodeEditor(
            parent=self, setting=self._editor_setting)

        self.layout.setMenuBar(self.menubar)
        self.layout.addWidget(self.node_editor)

    def _init_node_editor_from_session(self):
        # TODO: init node editor from session
        pass


if __name__ == "__main__":
    @compute
    def Add(a: int, b: int) -> int:
        return a + b

    with Session() as session:
        with Flow() as flow:
            add1 = Add(name="add1")
            add2 = Add(name="add2")
            add3 = Add(name="add3")
            add1.O[0] >> add3.I[0]
            add2.O[0] >> add3.I[1]

    app = QtWidgets.QApplication(sys.argv)
    instance = SunmaoQt(session)
    instance.show()
    app.exec_()
