from easynode.model.node import Node
from easynode.model.port import Port as ViewPort
from easynode.model.edge import Edge
from sunmao.core.node import ComputeNode
from sunmao.core.connection import Connection


class ViewNode(Node):
    def __init__(self, name: str | None = None, **attrs) -> None:
        super().__init__(name, **attrs)
        self.core_node: ComputeNode | None = None


class ViewEdge(Edge):
    def __init__(self, port1: ViewPort, port2: ViewPort) -> None:
        super().__init__(port1, port2)
        self.core_edge: Connection | None = None


__all__ = [
    "ViewNode",
    "ViewPort",
    "ViewEdge",
]
