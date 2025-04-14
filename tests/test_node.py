from b_tree.node import KeyValuePair, LeafNode


def test_leaf_node_init():
    node: LeafNode = LeafNode(2)
    assert node.kv_pairs == []
    assert node.max_num_keys == 2


def test_leaf_node_insert():
    node: LeafNode = LeafNode(2)
    node.insert(1, 100)
    assert node.kv_pairs[0].key == 1
    assert node.kv_pairs[0].value == 100

    node.insert(2, 200)
    assert node.kv_pairs[1].key == 2
    assert node.kv_pairs[1].value == 200


def test_leaf_node_get():
    node: LeafNode = LeafNode(5)
    node.insert(1, 1)
    assert node.get(1) == 1
    assert node.get(2) is None
    node.insert(2, 2)
    assert node.get(2) == 2

def test_leaf_node_keys():
    node: LeafNode = LeafNode(5)
    node.insert(1, 1)
    node.insert(2, 2)
    assert node.keys() == [1, 2]

    node.insert(3, 3)
    assert node.keys() == [1, 2, 3]

def test_key_value_pair_init():
    kv_pair = KeyValuePair(1, 1)
    assert kv_pair.key == 1
    assert kv_pair.value == 1

    kv_pair = KeyValuePair("key", 100)
    assert kv_pair.key == "key"
    assert kv_pair.value == 100
