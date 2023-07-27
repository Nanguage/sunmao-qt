from easynode.node_editor import NodeEditor

from .model import ViewNode


class NodeEditor(NodeEditor):
    def create_node(
            self, type_name,
            node_name: str | None = None,
            **attrs) -> ViewNode:
        node = super().create_node(type_name, node_name, **attrs)
        return node

    def register_factory(self, *factories: type[ViewNode]) -> None:
        return super().register_factory(*factories)
