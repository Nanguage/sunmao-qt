import typing as T

from sunmao.core.node import ComputeNode
from sunmao.core.flow import Flow

from .easynode.model import (
    ViewNode, ViewEdge,
    ViewPort, ViewDataPort, ViewGraph,
)

if T.TYPE_CHECKING:
    from .main import SunmaoQt


class Converter:
    """For type conversion between sunmao-core and view(easynode)."""
    def __init__(self, parent: "SunmaoQt"):
        self.parent = parent

    def compute_node_cls2view_node_cls(
            self,
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

    def core_flow2view_graph(self, flow: "Flow") -> "ViewGraph":
        vgraph = ViewGraph()
        cnode_id2vnode = {}
        for cnode in flow.nodes.values():
            core_cls = cnode.__class__
            cls_name = core_cls.__name__
            if cls_name not in self.parent.core_node_classes:
                self.parent.register_node_class(core_cls)
            vnode = self.parent.node_editor.create_node(
                cls_name, node_name=cnode.name)
            self.parent.signal_binder.bind_node(vnode, cnode)
            vgraph.add_node(vnode)
            cnode_id2vnode[cnode.id] = vnode
        for cedge in flow.connections.values():
            cport_from = cedge.source
            cport_to = cedge.target
            vnode_from = cnode_id2vnode[cport_from.node.id]
            vnode_to = cnode_id2vnode[cport_to.node.id]
            vport_from = vnode_from.output_ports[cport_from.index]
            vport_to = vnode_to.input_ports[cport_to.index]
            vedge = ViewEdge(vport_from, vport_to)
            self.parent.signal_binder.bind_edge(vedge, cedge)
            vgraph.add_edge(vedge)
        self.parent.signal_binder.bind_graph(vgraph, flow)
        return vgraph
