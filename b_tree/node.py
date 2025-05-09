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
        children (list[Node[T]]): 子ノードのリスト。非葉ノードの場合のみ使用されます。
        t (int): B木の最小次数 (minimum degree)。各ノードは t-1 個、最大 2t-1 個のキーを持ちます (ルートノードを除く)。
        is_leaf (bool): このノードが葉ノードであるかどうかを示すフラグ。
    """

    def __init__(self, t: int, is_leaf: bool):
        self.items: list[KeyValuePair] = []
        self.children: list[Node[T]] = []
        self.t = t
        self.is_leaf = is_leaf

    def split_child(self, i: int, y: "Node[T]") -> None:
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
        z.items = y.items[self.t :]

        if not y.is_leaf:
            z.children = y.children[self.t :]

        y.items = y.items[: self.t - 1]

        if not y.is_leaf:
            y.children = y.children[: self.t]

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

    def delete(self, key: T) -> bool:
        """このノードまたはそのサブツリーからキーを削除します。

        Args:
            key: 削除するキー。

        Returns:
            削除が成功した場合は True、キーが見つからなかった場合は False。
        """
        idx = self._find_key(key)

        # キーがこのノードにある場合
        if idx < len(self.items) and self.items[idx].key == key:
            if self.is_leaf:
                self._delete_from_leaf(idx)
            else:
                self._delete_from_non_leaf(idx)
            return True
        
        # キーがこのノードにない場合
        if self.is_leaf:
            # 葉ノードでキーが見つからなければ、キーは存在しない
            return False
        
        # 子ノードで削除処理を継続するが、先に必要な準備を行う
        child_idx = idx
        return self._ensure_child_has_enough_keys_and_delete(child_idx, key)

    def _find_key(self, key: T) -> int:
        """ノード内で指定されたキーの位置を検索します。

        キーが存在しない場合、適切な子ノードのインデックスを返します。

        Args:
            key: 検索するキー。

        Returns:
            キーのインデックス、または適切な子ノードのインデックス。
        """
        idx = 0
        while idx < len(self.items) and self.items[idx].key < key:
            idx += 1
        return idx
    
    def _delete_from_leaf(self, idx: int) -> None:
        """葉ノードからキーを削除します。

        Args:
            idx: 削除するキーのインデックス。
        """
        del self.items[idx]
    
    def _delete_from_non_leaf(self, idx: int) -> None:
        """非葉ノードからキーを削除します。

        Args:
            idx: 削除するキーのインデックス。
        """
        key = self.items[idx].key
        
        # ケース 1: idx の位置のキーの前にある子ノードが t 個以上のキーを持つ場合
        if len(self.children[idx].items) >= self.t:
            # 前駆者を見つけて、それと交換し、前駆者を削除
            pred = self._get_predecessor(idx)
            self.items[idx] = pred
            self.children[idx].delete(pred.key)
        
        # ケース 2: idx+1 の位置のキーの後ろにある子ノードが t 個以上のキーを持つ場合
        elif len(self.children[idx + 1].items) >= self.t:
            # 後継者を見つけて、それと交換し、後継者を削除
            succ = self._get_successor(idx)
            self.items[idx] = succ
            self.children[idx + 1].delete(succ.key)
        
        # ケース 3: 両方の子ノードが t-1 個のキーしか持たない場合
        else:
            # 子ノードをマージして、そのマージされたノードで削除を続行
            self._merge_children(idx)
            # idx 番目のキーはマージされた子ノードに移動しているので、そこで削除を続行
            self.children[idx].delete(key)
    
    def _get_predecessor(self, idx: int) -> KeyValuePair:
        """指定されたインデックスにあるキーの前駆者を取得します。

        前駆者は、左の子ツリーの最も右にあるノードの最も右のキーです。

        Args:
            idx: キーのインデックス。

        Returns:
            前駆者のキーと値のペア。
        """
        current = self.children[idx]
        while not current.is_leaf:
            current = current.children[-1]
        return current.items[-1]
    
    def _get_successor(self, idx: int) -> KeyValuePair:
        """指定されたインデックスにあるキーの後継者を取得します。

        後継者は、右の子ツリーの最も左にあるノードの最も左のキーです。

        Args:
            idx: キーのインデックス。

        Returns:
            後継者のキーと値のペア。
        """
        current = self.children[idx + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.items[0]
    
    def _merge_children(self, idx: int) -> None:
        """idx 番目の子と idx+1 番目の子をマージします。

        Args:
            idx: マージする最初の子のインデックス。
        """
        child = self.children[idx]
        sibling = self.children[idx + 1]
        
        # idx 番目のキーを子ノードに移動
        child.items.append(self.items[idx])
        
        # 兄弟のすべてのキーと子を子ノードにコピー
        child.items.extend(sibling.items)
        if not sibling.is_leaf:
            child.children.extend(sibling.children)
        
        # idx 番目のキーと idx+1 番目の子を削除
        del self.items[idx]
        del self.children[idx + 1]
    
    def _ensure_child_has_enough_keys_and_delete(self, idx: int, key: T) -> bool:
        """指定された子ノードが最低 t 個のキーを持つようにしてから、削除を続行します。

        Args:
            idx: 子ノードのインデックス。
            key: 削除するキー。

        Returns:
            削除が成功したかどうか。
        """
        # 子ノードが t-1 個のキーしかない場合
        if len(self.children[idx].items) == self.t - 1:
            # ケース 1: 隣接する兄弟が t 個以上のキーを持つ場合は、キーを借りる
            if idx > 0 and len(self.children[idx - 1].items) >= self.t:
                self._borrow_from_prev(idx)
            elif idx < len(self.children) - 1 and len(self.children[idx + 1].items) >= self.t:
                self._borrow_from_next(idx)
            # ケース 2: 両方の隣接する兄弟が t-1 個のキーしかない場合は、マージする
            else:
                if idx == len(self.children) - 1:
                    # 最後の子の場合は前の子とマージ
                    self._merge_children(idx - 1)
                    idx = idx - 1
                else:
                    self._merge_children(idx)
        
        # 子ノードでの削除を続行
        return self.children[idx].delete(key)
    
    def _borrow_from_prev(self, idx: int) -> None:
        """前の兄弟からキーを借りて、子ノードに追加します。

        Args:
            idx: 子ノードのインデックス。
        """
        child = self.children[idx]
        sibling = self.children[idx - 1]
        
        # 親のキーを子に移動
        child.items.insert(0, self.items[idx - 1])
        
        # 兄弟の最後のキーを親に移動
        self.items[idx - 1] = sibling.items.pop()
        
        # 兄弟が葉ノードでない場合、最後の子を子ノードに移動
        if not sibling.is_leaf:
            child.children.insert(0, sibling.children.pop())
    
    def _borrow_from_next(self, idx: int) -> None:
        """次の兄弟からキーを借りて、子ノードに追加します。

        Args:
            idx: 子ノードのインデックス。
        """
        child = self.children[idx]
        sibling = self.children[idx + 1]
        
        # 親のキーを子に移動
        child.items.append(self.items[idx])
        
        # 兄弟の最初のキーを親に移動
        self.items[idx] = sibling.items.pop(0)
        
        # 兄弟が葉ノードでない場合、最初の子を子ノードに移動
        if not sibling.is_leaf:
            child.children.append(sibling.children.pop(0))
