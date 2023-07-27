import sys
import typing as T

from qtpy import QtWidgets
from sunmao.api import Session, Flow, compute
from sunmao.core.node import ComputeNode

from .ui.menubar import Menubar
from .converter import Converter
from .signal_binder import SignalBinder
from .easynode.node_editor import NodeEditor
from .easynode import EditorSetting


class SunmaoQt(QtWidgets.QWidget):
    current_instance = None
    core_node_classes = {}

    def __init__(
            self,
            session: T.Optional[Session] = None,
            editor_setting: T.Optional[EditorSetting] = None):
        super().__init__()
        self._editor_setting = editor_setting
        self.__class__.current_instance = self
        self._init_ui()
        if session is None:
            session = Session()
        self.session = session
        self.converter = Converter(parent=self)
        self.signal_binder = SignalBinder(parent=self)
        self._init_node_editor_from_session()

    def _init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.menubar = Menubar(parent=self)
        self.node_editor = NodeEditor(
            parent=self, setting=self._editor_setting,
            init_scene=False)

        self.layout.setMenuBar(self.menubar)
        self.layout.addWidget(self.node_editor)

    def register_node_class(self, *node_cls: T.Type[ComputeNode]):
        for ncls in node_cls:
            view_node_cls = self.converter.compute_node_cls2view_node_cls(ncls)
            self.node_editor.register_factory(view_node_cls)
            self.core_node_classes[ncls.__name__] = ncls

    def _init_node_editor_from_session(self):
        for _, flow in self.session.flows.items():
            scene, _ = self.node_editor.add_scene_and_view(
                tab_name=flow.name)
            graph = self.converter.core_flow2view_graph(flow)
            scene.graph = graph
            scene.graph.auto_layout()


if __name__ == "__main__":
    @compute
    def Add(a, b: int) -> int:
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
