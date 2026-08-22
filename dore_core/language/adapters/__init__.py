"""Language adapters shipped with Doré."""
from .original_biblical import OSHBAdapter, MorphGNTAdapter
from .lxx_textfabric import LXXTextFabricAdapter
from .vulgate_json import VulgateJSONAdapter

__all__ = ["OSHBAdapter", "MorphGNTAdapter", "LXXTextFabricAdapter", "VulgateJSONAdapter"]
