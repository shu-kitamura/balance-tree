from typing import Generic, TypeVar

T = TypeVar("T")


class KeyValuePair(Generic[T]):
    """Node に格納される Key と Value のペアを表すクラス。

    Attributes:
        key (T): ペアのキー。 T は比較可能な型である必要がある。
        value (int): ペアの値。
    """
    def __init__(self, key: T, value: int) -> None:
        self.key = key
        self.value = value

    def __str__(self) -> str:
        return f"KeyValuePair({self.key}, {self.value})"


class Node(Generic[T]):
    """B木のノードを表すクラス。

    Attributes:
        items (list[KeyValuePair]): ノードに格納されているキーと値のペアのリスト。キーでソートされています。
        children (list['Node[T]']): 子ノードのリスト。非葉ノードの場合のみ使用されます。
        t (int): B木の最小次数 (minimum degree)。各ノードは 최소 t-1 個、最大 2t-1 個のキーを持ちます (ルートノードを除く)。
        is_leaf (bool): このノードが葉ノードであるかどうかを示すフラグ。
    """
    def __init__(self, t: int, is_leaf: bool):
        self.items: list[KeyValuePair] = []
        self.children: list['Node[T]'] = []
        self.t = t
        self.is_leaf = is_leaf

    def split_child(self, i: int, y: 'Node[T]') -> None:
        """子ノード を分割します。

        このメソッドは、子ノード y が満杯 (2t-1 個のキーを持つ) の場合に呼び出されることを想定している。
        分割により y の中央のキーがこのノード (self) に昇格し、
        y の後半のキーと子ノード (存在する場合) が新しいノード z に移動します。
        新しいノード z は、このノード (self) の子リストの y の直後に挿入されます。

        Args:
            i: self.children における子ノード y のインデックス。
            y: 分割対象の子ノード
        """
        z: Node = Node(y.t, y.is_leaf)
        middle_kv_pair = y.items[self.t - 1]
        z.items = y.items[self.t:]

        if not y.is_leaf:
            z.children = y.children[self.t:]

        y.items = y.items[:self.t - 1]

        if not y.is_leaf:
            y.children = y.children[:self.t]

        self.children.insert(i + 1, z)
        self.items.insert(i, middle_kv_pair)

    def insert(self, kv_pair: KeyValuePair[T]) -> None:
        """キーと値のペアをこのノード (またはそのサブツリー) に挿入します。

        このメソッドは、このノードが満杯でないことを前提としています。
        ルートノードが満杯の場合は、B木のメインクラスで処理する必要があります。
        ノードが葉か非葉かに応じて、適切なヘルパーメソッドに処理を委譲します。

        Args:
            kv_pair: 挿入するキーと値のペア。
        """
        if self.is_leaf:
            self.__insert_to_leaf(kv_pair)
        else:
            self.__insert_to_non_leaf(kv_pair)

    def __insert_to_leaf(self, kv_pair: KeyValuePair[T]) -> None:
        """キーと値のペアを葉ノードに挿入します。

        キーの順序を維持するように、適切な位置に挿入します。
        このメソッドは、葉ノードが満杯でないことを前提としています。

        Args:
            kv_pair: 挿入するキーと値のペア。
        """
        insert_index = self.__find_insert_index(kv_pair.key)
        self.items.insert(insert_index, kv_pair)

    def __insert_to_non_leaf(self, kv_pair: KeyValuePair[T]) -> None:
        """キーと値のペアを非葉ノードに挿入します。

        挿入するキーに基づいて適切な子ノードを検索します。
        もしその子ノードが満杯であれば、`split_child` を呼び出して分割します。
        分割後、再度適切な子ノードを決定し、その子ノードに対して再帰的に挿入処理を呼び出します。

        Args:
            kv_pair: 挿入するキーと値のペア。
        """
        child_index = self.__find_insert_index(kv_pair.key)

        child = self.children[child_index]
        if len(child.items) == (2 * self.t - 1):
            self.split_child(child_index, child)

            if kv_pair.key > self.items[child_index].key:
                child_index += 1

        self.children[child_index].insert(kv_pair)

    def __find_insert_index(self, key: T) -> int:
        """挿入するキーのインデックスを見つけるヘルパー関数"""
        i = len(self.items) - 1
        while i >= 0 and key < self.items[i].key:
            i -= 1
        return i + 1