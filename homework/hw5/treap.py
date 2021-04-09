from typing import Tuple, TypeVar, Optional, MutableMapping, Iterator, List

from homework.hw5.node import Node

K = TypeVar("K")
V = TypeVar("V")


class Treap(MutableMapping):
    def __init__(self):
        self.root: Optional[Node[K, V]] = None
        self.keys: List[K] = []
        self.values: List[V] = []

    def __setitem__(self, key: K, value: V):
        if key in self.keys:
            raise ValueError(f"Treap already contains key {key}")
        elif value in self.values:
            raise ValueError(f"Treap already contains priority {value}")
        if self.root is None:
            self.root = Node(key, value)
        else:
            self.root = self.root.insert(key, value)
        self.keys.append(key)
        self.values.append(value)

    def __getitem__(self, key: K) -> V:
        if self.root is None:
            raise KeyError(f"Treap does not contain key {key}")
        return self.root[key]

    def __delitem__(self, key: K):
        value = self[key]
        self.root = self.root.remove(key)
        self.keys.remove(key)
        self.values.remove(value)

    def __contains__(self, key: K):
        if self.root is None:
            return False
        return key in self.root

    def __iter__(self) -> Iterator[Tuple[K, V]]:
        return map(lambda x: x[0], self.root.__iter__())

    def backward_iterator(self) -> Iterator[Tuple[K, V]]:
        return self.root.backward_order()

    def __len__(self):
        return len(self.root)

    def forward_iterator(self) -> Iterator[Tuple[K, V]]:
        return self.root.forward_order()
