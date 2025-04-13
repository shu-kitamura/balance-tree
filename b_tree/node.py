class LeafNode:
    """A class representing a leaf node in a B-tree."""

    def __init__(self, min: int):
        self.kv_pairs: dict = {}
        self.min_num_keys: int = min  # The minimum number of keys in the node.

    def __str__(self):
        return f"LeafNode(is_leaf={self.is_leaf}, keys={self.keys}, num_keys={self.num_keys})"

    def insert(self, key: int, value: int):
        """Insert a key-value pair into the leaf node."""

        self.kv_pairs[key] = value
        # TODO: split the node
        if len(self.kv_pairs) > (2 * self.min_num_keys) - 1:
            # self.split()
            pass
