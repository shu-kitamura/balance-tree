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

    # TODO: search, delete などのメソッドを実装
