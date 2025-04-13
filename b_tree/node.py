from typing import Generic, TypeVar

T = TypeVar("T")


class LeafNode(Generic[T]):
    """A class representing a leaf node in a B-tree."""

    def __init__(self, min: int) -> None:
        self.kv_pairs: dict[T, int] = {}
        self.min_num_keys: int = min  # The minimum number of keys in the node.

    def __str__(self) -> str:
        return f"LeafNode({self.kv_pairs}, min_num_keys={self.min_num_keys})"

    def insert(self, key: T, value: int) -> None:
        """Insert a key-value pair into the leaf node."""

        self.kv_pairs[key] = value
        # TODO: split the node
        if len(self.kv_pairs) > (2 * self.min_num_keys) - 1:
            # self.split()
            pass
