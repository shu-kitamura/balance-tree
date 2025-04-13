def test_node_init():
    from b_tree.node import Node

    # Test case 1: Initialize a leaf node with min_num_keys = 2
    leaf_node: Node = Node(min=2, is_leaf=True)
    assert leaf_node.is_leaf
    assert leaf_node.keys == []
    assert leaf_node.children == []
    assert leaf_node.min_num_keys == 2

    # Test case 2: Initialize a non-leaf node with min_num_keys = 3
    non_leaf_node: Node = Node(min=3, is_leaf=False)
    assert not non_leaf_node.is_leaf
    assert non_leaf_node.keys == []
    assert non_leaf_node.children == []
    assert non_leaf_node.min_num_keys == 3
