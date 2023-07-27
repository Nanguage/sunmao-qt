import typing as T
from sunmao.core.node import ComputeNode
from sunmao.core.connection import Connection
from sunmao.core.flow import Flow

from .easynode.model import ViewNode, ViewEdge, ViewGraph
from .utils import logger

if T.TYPE_CHECKING:
    from .main import SunmaoQt


class SignalBinder:
    """Bind signals to easynode's slots."""
    def __init__(self, parent: "SunmaoQt"):
        self.parent = parent

    def bind_node(self, vnode: "ViewNode", cnode: "ComputeNode"):
        """Bind signals to a ViewNode."""
        if vnode.core_node is None:
            vnode.core_node = cnode
            for vport in vnode.input_ports + vnode.output_ports:
                vport.edge_added.connect(
                    vport._on_edge_added,
                )

    def bind_edge(self, vedge: "ViewEdge", cedge: "Connection"):
        """Bind signals to a ViewEdge."""
        if vedge.core_edge is None:
            vedge.core_edge = cedge

    def bind_graph(self, vgraph: "ViewGraph", cgraph: "Flow"):
        """Bind signals to a ViewGraph."""
        if vgraph.core_graph is None:
            vgraph.core_graph = cgraph

            def _on_edge_added(vedge: "ViewEdge"):
                vedge = ViewEdge.cast(vedge)
                cedge = self.parent.converter.view_edge2core_edge(vedge)
                cgraph.add_obj(cedge)
                self.bind_edge(vedge, cedge)
            vgraph.edge_added.connect(_on_edge_added)

            def _on_edge_removed(vedge: "ViewEdge"):
                cedge = vedge.core_edge
                cgraph.remove_obj(cedge)
                vedge.core_edge = None
            vgraph.edge_removed.connect(_on_edge_removed)

            def _on_node_added(vnode: "ViewNode"):
                cnode = self.parent.converter.view_node2core_node(vnode)
                cgraph.add_obj(cnode)
                self.bind_node(vnode, cnode)
            vgraph.node_added.connect(_on_node_added)

            def _on_node_removed(vnode: "ViewNode"):
                cnode = vnode.core_node
                cgraph.remove_obj(cnode)
                vnode.core_node = None
            vgraph.node_removed.connect(_on_node_removed)

            def _on_elements_changed():
                logger.debug("Elements changed.")
                logger.debug(f"Current nodes: {cgraph.nodes}")
                logger.debug(f"Current edges: {cgraph.connections}")
            vgraph.elements_changed.connect(_on_elements_changed)
