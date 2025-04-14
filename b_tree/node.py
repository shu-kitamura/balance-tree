from typing import Generic, TypeVar

T = TypeVar("T")


class KeyValuePair(Generic[T]):
    """A class representing a key-value pair."""

    def __init__(self, key: T, value: int) -> None:
        self.key = key  # The key of the pair.
        self.value = value  # The value of the pair.

    def __str__(self) -> str:
        return f"KeyValuePair({self.key}, {self.value})"


class LeafNode(Generic[T]):
    """A class representing a leaf node in a B-tree."""

    def __init__(self, max: int) -> None:
        self.kv_pairs: list[KeyValuePair] = []
        self.max_num_keys: int = max  # The maximum number of keys in the node.

    def __str__(self) -> str:
        return f"LeafNode({self.kv_pairs}, min_num_keys={self.max_num_keys})"

    def insert(self, key: T, value: int) -> None:
        """Insert a key-value pair into the leaf node."""
        i = 0
        while i < len(self.kv_pairs) and self.kv_pairs[i].key < key:
            i += 1

        self.kv_pairs.insert(i, KeyValuePair(key, value))

    def get(self, key: T) -> int | None:
        """Get the value associated with a key in the leaf node."""
        for kv_pair in self.kv_pairs:
            if kv_pair.key == key:
                return kv_pair.value
        return None
