from typing import Generic, TypeVar

T = TypeVar("T")


class KeyValuePair(Generic[T]):
    """A class representing a key-value pair."""

    def __init__(self, key: T, value: int) -> None:
        self.key = key  # The key of the pair.
        self.value = value  # The value of the pair.

    def __str__(self) -> str:
        return f"KeyValuePair({self.key}, {self.value})"


class Node(Generic[T]):
    """A class representing a node in a B-tree."""

    def __init__(self, t: int, is_leaf: bool):
        self.items: list[KeyValuePair] = []
        self.children: list[Node] = []
        self.t = t
        self.is_leaf = is_leaf

    def insert(self, kv_pair: KeyValuePair[T]) -> None:
        """Insert a key-value pair into the node."""

        if self.is_leaf:
            self.__insert_to_leaf(kv_pair)
        else:
            self.__insert_to_non_leaf(kv_pair)

    def __insert_to_leaf(self, kv_pair: KeyValuePair[T]) -> None:
        """Insert a key-value pair into a leaf node."""
        i = len(self.items) - 1
        while i >= 0 and kv_pair.key < self.items[i].key:
            i -= 1

        self.items.insert(i + 1, kv_pair)

    def __insert_to_non_leaf(self, kv_pair: KeyValuePair[T]) -> None:
        """Insert a key-value pair into a non-leaf node."""
        i = len(self.items) - 1
        while i >= 0 and kv_pair.key < self.items[i].key:
            i -= 1
        self.children[i].insert(kv_pair)
