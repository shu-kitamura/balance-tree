from typing import Generic, TypeVar

from .node import KeyValuePair, Node

T = TypeVar("T")


class BTree(Generic[T]):
    """B木全体を表すクラス。

    Attributes:
        root (Optional[Node[T]]): B木のルートノード。最初は None。
        t (int): B木の最小次数 (minimum degree)。
    """

    def __init__(self, t: int):
        """B木を初期化します。

        Args:
            t: B木の最小次数。t >= 2 である必要があります。
        """
        if t < 2:
            raise ValueError("B木の最小次数 t は 2 以上である必要があります。")
        self.root: Node[T] = Node(t, True)
        self.t = t

    def insert(self, key: T, value: int) -> None:
        """B木に新しいキーと値のペアを挿入します。

        Args:
            key: 挿入するキー。
            value: 挿入する値。
        """
        kv_pair = KeyValuePair(key, value)
        root = self.root

        # ルートノードが満杯の場合
        if len(root.items) == (2 * self.t - 1):
            # 新しいルートノードを作成
            new_root = Node(self.t, False)  # 新しいルートは非葉ノード
            new_root.children.append(root)  # 古いルートを子にする
            self.root = new_root
            # 古いルートノードを分割する
            new_root.split_child(0, root)
            # 新しいキーを挿入する適切な子ノードを決定する
            # split_child によって new_root にキーが1つ昇格している
            if kv_pair.key > new_root.items[0].key:
                # 新しいキーは右側の子 (分割によって新しくできたノード) に挿入
                new_root.children[1].insert(kv_pair)
            else:
                # 新しいキーは左側の子 (元のルート) に挿入
                new_root.children[0].insert(kv_pair)
        # ルートノードが満杯でない場合
        else:
            root.insert(kv_pair)

    def search(self, key: T) -> tuple[Node[T], int] | None:
        """キーを検索します。

        Args:
            key: 検索するキー。

        Returns:
            キーが見つかった場合は (ノード, キーのインデックス) のタプル、見つからなかった場合は None。
        """
        if not self.root:
            return None
        return self._search_node(self.root, key)

    def _search_node(self, node: Node[T], key: T) -> tuple[Node[T], int] | None:
        """指定したノードとそのサブツリー内でキーを検索します。

        Args:
            node: 検索を開始するノード。
            key: 検索するキー。

        Returns:
            キーが見つかった場合は (ノード, キーのインデックス) のタプル、見つからなかった場合は None。
        """
        # ノード内でキーを検索
        i = 0
        while i < len(node.items) and key > node.items[i].key:
            i += 1

        # キーが見つかった場合
        if i < len(node.items) and key == node.items[i].key:
            return (node, i)

        # キーが見つからず、葉ノードの場合は存在しない
        if node.is_leaf:
            return None

        # 適切な子ノードで再帰的に検索
        return self._search_node(node.children[i], key)

    def update(self, key: T, value: int) -> bool:
        """既存のキーに関連付けられた値を更新します。

        Args:
            key: 更新するキー。
            value: 新しい値。

        Returns:
            更新が成功した場合はTrue、キーが見つからなかった場合はFalse。
        """
        result = self.search(key)
        if result is None:
            return False

        node, idx = result
        node.items[idx].value = value
        return True

    def delete(self, key: T) -> bool:
        """B木からキーを削除します。

        Args:
            key: 削除するキー。

        Returns:
            削除が成功した場合は True、キーが見つからなかった場合は False。
        """
        if not self.root:
            return False
        
        result = self.root.delete(key)
        
        # ルートノードがキーを持たなくなった場合、
        # かつ子ノードが1つだけある場合、ツリーの高さを減らす
        if len(self.root.items) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]
        
        return result
