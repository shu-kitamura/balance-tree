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

def test_node_insert_to_non_leaf_without_split():
    t = 3
    node = Node(t, False)
    # items: キー k < 10 の要素は children[0] へ
    #        10 <= k < 20 の要素は children[1] へ
    #        k >= 20 の要素は children[2] へ
    node.items.append(KeyValuePair(10, 100))
    node.items.append(KeyValuePair(20, 200))
    # items = [ (10, 100), (20, 200) ] -> len = 2

    # children は len(items) + 1 = 3 つ必要
    child0 = Node(t, True) # Keys < 10
    child0.items.append(KeyValuePair(1, 10))
    child0.items.append(KeyValuePair(5, 50))

    child1 = Node(t, True) # 10 <= Keys < 20
    child1.items.append(KeyValuePair(12, 120))
    child1.items.append(KeyValuePair(15, 150))

    child2 = Node(t, True) # Keys >= 20
    child2.items.append(KeyValuePair(22, 220))
    child2.items.append(KeyValuePair(25, 250))

    node.children.append(child0)
    node.children.append(child1)
    node.children.append(child2) # 3番目の子ノードを追加
    # children = [ child0, child1, child2 ] -> len = 3

    # 挿入 1: kv_pair = (7, 70) -> child0 へ
    node.insert(KeyValuePair(7, 70))
    assert len(child0.items) == 3
    assert child0.items[0].key == 1
    assert child0.items[1].key == 5
    assert child0.items[2].key == 7 # 正しい位置に挿入されたか確認

    # 挿入 2: kv_pair = (18, 180) -> child1 へ
    node.insert(KeyValuePair(18, 180))
    assert len(child1.items) == 3
    assert child1.items[0].key == 12
    assert child1.items[1].key == 15
    assert child1.items[2].key == 18 # 正しい位置に挿入されたか確認

    # 挿入 3: kv_pair = (28, 280) -> child2 へ
    node.insert(KeyValuePair(28, 280))
    assert len(child2.items) == 3
    assert child2.items[0].key == 22
    assert child2.items[1].key == 25
    assert child2.items[2].key == 28 # 正しい位置に挿入されたか確認

def test_node_insert_to_non_leaf_with_split():
    t = 2 # 最小次数 t=2 -> ノードは最大 2*t-1 = 3 つのキーを持つ
    node = Node(t, False)
    node.items.append(KeyValuePair(10, 100)) # items = [(10, 100)]

    child0 = Node(t, True) # Keys < 10
    child0.items.append(KeyValuePair(1, 10))
    child0.items.append(KeyValuePair(5, 50))
    child0.items.append(KeyValuePair(8, 80)) # child0 は満杯 (3 keys)

    child1 = Node(t, True) # Keys >= 10
    child1.items.append(KeyValuePair(12, 120))
    child1.items.append(KeyValuePair(15, 150))

    node.children.append(child0)
    node.children.append(child1) # children = [child0, child1]

    # 挿入: kv_pair = (3, 30) -> child0 に挿入されるべき -> split が発生
    node.insert(KeyValuePair(3, 30))

    # 結果の確認
    # 親ノード (node)
    assert len(node.items) == 2
    assert node.items[0].key == 5 # child0 から昇格したキー
    assert node.items[1].key == 10
    assert len(node.children) == 3 # 子が1つ増えた

    # 元の child0 (分割後)
    child0_after_split = node.children[0]
    assert len(child0_after_split.items) == 2
    assert child0_after_split.items[0].key == 1
    assert child0_after_split.items[1].key == 3 # 挿入されたキー

    # 新しく作られたノード z
    new_child_z = node.children[1]
    assert len(new_child_z.items) == 1
    assert new_child_z.items[0].key == 8

    # 元の child1
    child1_original = node.children[2]
    assert len(child1_original.items) == 2
    assert child1_original.items[0].key == 12
    assert child1_original.items[1].key == 15
