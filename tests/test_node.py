from b_tree.node import KeyValuePair, Node


def test_key_value_pair_init():
    kv_pair = KeyValuePair(1, 1)
    assert kv_pair.key == 1
    assert kv_pair.value == 1

    kv_pair = KeyValuePair("key", 100)
    assert kv_pair.key == "key"
    assert kv_pair.value == 100


def test_node_init():
    node = Node(2, True)
    assert node.is_leaf is True
    assert node.t == 2
    assert node.items == []
    assert node.children == []


def test_node_insert_to_leaf():
    node = Node(5, True)

    node.insert(KeyValuePair(1, 100))
    assert len(node.items) == 1
    item = node.items[0]
    assert (item.key, item.value) == (1, 100)

    node.insert(KeyValuePair(10, 200))
    assert len(node.items) == 2
    item = node.items[1]
    assert (item.key, item.value) == (10, 200)

    node.insert(KeyValuePair(5, 300))
    assert len(node.items) == 3
    item = node.items[1]
    assert (item.key, item.value) == (5, 300)


def test_node_insert_to_non_leaf():
    node = Node(3, False)
    node.items.append(KeyValuePair(1, 10))
    node.items.append(KeyValuePair(10, 100))
    node.items.append(KeyValuePair(20, 200))

    leaf_node1 = Node(3, True)
    leaf_node1.items.append(KeyValuePair(3, 30))
    leaf_node1.items.append(KeyValuePair(7, 70))

    leaf_node2 = Node(3, True)
    leaf_node2.items.append(KeyValuePair(12, 120))
    leaf_node2.items.append(KeyValuePair(17, 170))

    node.children.append(leaf_node1)
    node.children.append(leaf_node2)

    node.insert(KeyValuePair(5, 50))
    node.insert(KeyValuePair(15, 150))

    child = node.children[0]  # should be leaf_node1
    assert len(child.items) == 3
    item = child.items[1]
    assert (item.key, item.value) == (5, 50)

    child = node.children[1]  # should be leaf_node2
    assert len(child.items) == 3
    item = child.items[1]
    assert (item.key, item.value) == (15, 150)
