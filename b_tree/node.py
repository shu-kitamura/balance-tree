class Node:
    def __init__(self, min: int, is_leaf: bool = True):
        self.is_leaf: bool = is_leaf # If the node is a leaf.
        self.keys: list = [] # The keys in the node.
        self.children: list = [] # The children of the node.
        self.min_num_keys: int = min # The minimum number of keys in the node.

    def __str__(self):
        return (
            f"Node(is_leaf={self.is_leaf}, keys={self.keys}, num_keys={self.num_keys})"
        )
