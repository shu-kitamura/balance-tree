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

    def __init__(self, is_leaf: bool, t: int):
        self.items: list[KeyValuePair] = []
        self.children: list[Node] = []
        self.is_leaf: bool = is_leaf
        self.t = t
