"""Language adapters shipped with Doré."""
from .original_biblical import OSHBAdapter, MorphGNTAdapter
from .lxx_textfabric import LXXTextFabricAdapter

__all__ = ["OSHBAdapter", "MorphGNTAdapter", "LXXTextFabricAdapter"]
