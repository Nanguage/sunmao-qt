import sys
import typing as T

from qtpy import QtWidgets
from easynode.node_editor import NodeEditor
from easynode.setting import EditorSetting
from easynode.model import Node as ViewNode
from easynode.model.port import Port as ViewPort
from easynode.model.port import DataPort as ViewDataPort
from easynode.model.edge import Edge as ViewEdge
from sunmao.api import Session, Flow, compute
from sunmao.core.node import ComputeNode

from .ui.menubar import Menubar


def compute_node2view_node(
        cnode: T.Type[ComputeNode]
        ) -> T.Type[ViewNode]:
    """Convert a ComputeNode to a ViewNode."""
    view_in_ports = []
    view_out_ports = []
    for tp in ('in', 'out'):
        if tp == 'in':
            cports = cnode.init_input_ports
            vports = view_in_ports
        else:
            cports = cnode.init_output_ports
            vports = view_out_ports
        for inp in cports:
            if tp == 'in':
                if inp.type is None:
                    vp = ViewPort(name=inp.name)
                else:
                    vp = ViewDataPort(
                        name=inp.name,
                        data_type=inp.type,
                        data_range=inp.range,
                        data_default=inp.default,
                    )
            else:
                vp = ViewPort(name=inp.name)
            vports.append(vp)

    class NewViewNode(ViewNode):
        input_ports = view_in_ports
        output_ports = view_out_ports

    NewViewNode.__name__ = cnode.__name__
    return NewViewNode


class SunmaoQt(QtWidgets.QWidget):
    current_instance = None
    core_node_classes = {}

    def __init__(
            self,
            session: Session,
            editor_setting: T.Optional[EditorSetting] = None):
        super().__init__()
        self._editor_setting = editor_setting
        self.__class__.current_instance = self
        self._init_ui()
        self.session = session
        self._init_node_editor_from_session()

    def _init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.menubar = Menubar(parent=self)
        self.node_editor = NodeEditor(
            parent=self, setting=self._editor_setting,
            init_scene=False)

        self.layout.setMenuBar(self.menubar)
        self.layout.addWidget(self.node_editor)

    def register_node(self, *node_cls: T.Type[ComputeNode]):
        for ncls in node_cls:
            view_node_cls = compute_node2view_node(ncls)
            self.node_editor.factory_table.register(view_node_cls)
            self.core_node_classes[ncls.__name__] = ncls

    def _init_node_editor_from_session(self):
        for _, flow in self.session.flows.items():
            scene, _ = self.node_editor.add_scene_and_view(
                tab_name=flow.name)
            cnode_id2vnode = {}
            for cnode in flow.nodes.values():
                core_cls = cnode.__class__
                cls_name = core_cls.__name__
                if cls_name not in self.core_node_classes:
                    self.register_node(core_cls)
                vnode = self.node_editor.create_node(cls_name)
                scene.graph.add_node(vnode)
                cnode_id2vnode[cnode.id] = vnode
            for cedge in flow.connections.values():
                cport_from = cedge.source
                cport_to = cedge.target
                vnode_from = cnode_id2vnode[cport_from.node.id]
                vnode_to = cnode_id2vnode[cport_to.node.id]
                vport_from = vnode_from.output_ports[cport_from.index]
                vport_to = vnode_to.input_ports[cport_to.index]
                vedge = ViewEdge(vport_from, vport_to)
                scene.graph.add_edge(vedge)
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
