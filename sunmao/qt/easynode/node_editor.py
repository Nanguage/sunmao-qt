from easynode.node_editor import NodeEditor
from sunmao.core.session import Session

from .model import ViewNode


class NodeEditor(NodeEditor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.core_session: Session | None = None

    def create_node(
            self, type_name,
            node_name: str | None = None,
            **attrs) -> ViewNode:
        node = super().create_node(type_name, node_name, **attrs)
        return node

    def register_factory(self, *factories: type[ViewNode]) -> None:
        return super().register_factory(*factories)
