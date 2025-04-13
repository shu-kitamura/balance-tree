class Node:
    def __init__(self, min: int, is_leaf: bool = True):
        self.is_leaf: bool = is_leaf
        self.keys: list = []
        self.children: list = []
        self.min_num_keys: int = min

    def __str__(self):
        return (
            f"Node(is_leaf={self.is_leaf}, keys={self.keys}, num_keys={self.num_keys})"
        )
