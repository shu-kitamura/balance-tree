from b_tree.node import KeyValuePair, Node


def test_key_value_pair_init():
    kv_pair = KeyValuePair(1, 1)
    assert kv_pair.key == 1
    assert kv_pair.value == 1

    kv_pair = KeyValuePair("key", 100)
    assert kv_pair.key == "key"
    assert kv_pair.value == 100


def test_node_init():
    node = Node(2)
    assert node.is_leaf is True
    assert node.t == 2
    assert node.items == []
    assert node.children == []
