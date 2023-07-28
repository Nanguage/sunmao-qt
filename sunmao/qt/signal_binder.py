import typing as T
from sunmao.core.node import ComputeNode
from sunmao.core.connection import Connection
from sunmao.core.flow import Flow

from .easynode import GraphicsScene
from .easynode.model import ViewNode, ViewEdge, ViewGraph
from .easynode.node_editor import NodeEditor
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
            vnode.renamed.connect(vnode._on_name_changed)
            # bind signals to ports
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
                logger.debug(f"Flow({cgraph.name}) elements changed.")
                logger.debug(f"Nodes: {cgraph.nodes}")
                logger.debug(f"Edges: {cgraph.connections}")
            vgraph.elements_changed.connect(_on_elements_changed)

    def bind_editor(self, editor: "NodeEditor"):
        """Bind signals to a NodeEditor."""
        if editor.core_session is None:
            editor.core_session = self.parent.session

            def _on_add_scene(scene: "GraphicsScene"):
                vgraph = scene.graph = ViewGraph()
                cgraph = self.parent.converter.new_core_flow()
                print(cgraph.name)
                editor.tabs.setTabText(
                    editor.tabs.count() - 1,
                    cgraph.name)
                self.bind_graph(vgraph, cgraph)
            editor.scene_added.connect(_on_add_scene)
