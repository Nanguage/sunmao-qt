import typing as T
from easynode.model import Node as ViewNode

if T.TYPE_CHECKING:
    from .main import SunmaoQt


class SignalBinder:
    """Bind signals to easynode's slots."""
    def __init__(self, parent: "SunmaoQt"):
        self.parent = parent

    def bind_node(self, node: "ViewNode"):
        """Bind signals to a ViewNode."""
        pass
