import pytest

from b_tree.b_tree import BTree


def test_btree_init_valid():
    """有効な最小次数で BTree の初期化をテストします。"""
    t = 2
    tree = BTree(t)
    assert tree.t == t
    assert tree.root is not None
    assert tree.root.is_leaf is True
    assert len(tree.root.items) == 0
    assert len(tree.root.children) == 0


def test_btree_init_invalid():
    """無効な最小次数で BTree の初期化をテストします。"""
    with pytest.raises(ValueError):
        BTree(1)
    with pytest.raises(ValueError):
        BTree(0)
    with pytest.raises(ValueError):
        BTree(-1)


def test_btree_insert_empty_tree():
    """空の木に最初の要素を挿入するテスト。"""
    tree = BTree(t=2)
    tree.insert(10, 100)
    assert tree.root is not None
    assert len(tree.root.items) == 1
    assert tree.root.items[0].key == 10
    assert tree.root.items[0].value == 100
    assert tree.root.is_leaf is True


def test_btree_insert_non_full_root_leaf():
    """満杯でないルートノード（葉）への挿入をテストします。"""
    tree = BTree(t=2)  # ルートの最大キー数 = 2*t - 1 = 3
    tree.insert(10, 100)
    tree.insert(20, 200)
    assert len(tree.root.items) == 2
    assert tree.root.items[0].key == 10
    assert tree.root.items[1].key == 20

    tree.insert(5, 50)  # より小さいキーを挿入
    assert len(tree.root.items) == 3
    assert tree.root.items[0].key == 5
    assert tree.root.items[1].key == 10
    assert tree.root.items[2].key == 20
    assert tree.root.is_leaf is True


def test_btree_insert_full_root_leaf_split_revised():
    """満杯のルートノード（葉）への挿入による分割をテストします"""
    tree = BTree(t=2)  # 最大キー数 = 3
    tree.insert(10, 100)
    tree.insert(20, 200)
    tree.insert(5, 50)  # ルートが満杯: [ (5,50), (10,100), (20,200) ]

    # 15 を挿入、これにより分割が発生するはず
    tree.insert(15, 150)

    # 新しいルートを確認
    assert tree.root is not None
    assert tree.root.is_leaf is False
    assert len(tree.root.items) == 1
    assert tree.root.items[0].key == 10  # 中央のキーが昇格
    assert len(tree.root.children) == 2

    # 左の子（元のルート、分割後）を確認
    left_child = tree.root.children[0]
    assert left_child.is_leaf is True
    assert len(left_child.items) == 1  # 10 未満のキーのみを持つべき
    assert left_child.items[0].key == 5

    # 右の子（新しく作成されたノード z）を確認
    right_child = tree.root.children[1]
    assert right_child.is_leaf is True
    assert (
        len(right_child.items) == 2
    )  # 分割による 10 以上のキー + 挿入されたキーを持つべき
    assert right_child.items[0].key == 15  # 挿入されたキー
    assert right_child.items[1].key == 20
