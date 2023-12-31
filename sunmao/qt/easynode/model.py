from easynode.graphics.scene import GraphicsScene
from easynode.model.node import Node
from easynode.model.edge import Edge
from easynode.model.port import Port
from easynode.model.port import DataPort
from easynode.model.graph import Graph
from easynode.setting import PortSetting

from sunmao.core.flow import Flow
from sunmao.core.node import ComputeNode
from sunmao.core.connection import Connection


class ViewPort(Port):
    def __init__(
            self, name: str,
            setting: PortSetting | None = None) -> None:
        self.node: ViewNode
        super().__init__(name, setting)

    def _on_edge_added(self, edge: "ViewEdge") -> None:
        if self.type == "in":
            edge.source_port.node.core_node


class ViewDataPort(DataPort, ViewPort):
    def __init__(
            self, name: str,
            data_type: type = object,
            data_range: object = None,
            data_default: object = None,
            widget_args: dict[str, object] | None = None,
            setting: PortSetting | None = None) -> None:
        DataPort.__init__(
            self,
            name, data_type,
            data_range, data_default,
            widget_args, setting)


class ViewNode(Node):
    input_ports: list[ViewPort]
    output_ports: list[ViewPort]

    def __init__(self, name: str | None = None, **attrs) -> None:
        super().__init__(name, **attrs)
        self.core_node: ComputeNode | None = None

    def _on_name_changed(self, name: str) -> None:
        if self.core_node is not None:
            self.core_node.name = name


class ViewEdge(Edge):
    def __init__(self, port1: ViewPort, port2: ViewPort) -> None:
        self.source_port: ViewPort
        self.target_port: ViewPort
        super().__init__(port1, port2)
        self.core_edge: Connection | None = None

    @classmethod
    def cast(cls, edge: Edge) -> "ViewEdge":
        """Cast an EasyNode Edge to ViewEdge."""
        if isinstance(edge, cls):
            return edge
        return ViewEdge(edge.source_port, edge.target_port)


class ViewGraph(Graph):
    def __init__(
            self, scene: GraphicsScene | None = None
            ) -> None:
        super().__init__(scene)
        self.core_graph: Flow | None = None


__all__ = [
    "ViewGraph",
    "ViewNode",
    "ViewEdge",
    "ViewPort",
    "ViewDataPort",
]
