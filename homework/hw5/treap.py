from typing import Tuple, TypeVar, Optional, MutableMapping, Iterator, List

from homework.hw5.node import Node

K = TypeVar("K")
V = TypeVar("V")


class Treap(MutableMapping):
    """
    Class that represents Treap instance
    """

    def __init__(self):
        self.root: Optional[Node[K, V]] = None
        self.keys: List[K] = []
        self.values: List[V] = []

    def __setitem__(self, key: K, value: V):
        """
        Function that add new instance to Treap
        :param key: key of adding instance
        :param value: priority of adding instance
        """
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
        """
        Function that get instance from Treap by key
        :param key: key of instance to get
        :return: instance's priority
        """
        if self.root is None:
            raise KeyError(f"Treap does not contain key {key}")
        return self.root[key]

    def __delitem__(self, key: K):
        """
        Function that removes instance form Trap by key
        :param key: key of removing instance
        """
        value: K = self[key]
        if self.root is None:
            raise KeyError(f"Treap does not contain key {key}")
        self.root = self.root.remove(key)
        self.keys.remove(key)
        self.values.remove(value)

    def __contains__(self, key: K) -> bool:
        """
        Function that checks if instance with given key in the Treap
        :param key: key of checking instance
        """
        if self.root is None:
            return False
        return key in self.root

    def __iter__(self) -> Iterator[Tuple[K, V]]:
        """
        Function that return iterator of class
        :return: forward iterator
        """
        return self.forward_iterator()

    def backward_iterator(self) -> Iterator[Tuple[K, V]]:
        if self.root is None:
            raise ValueError("Treap is empty")
        return self.root.backward_order()

    def forward_iterator(self) -> Iterator[Tuple[K, V]]:
        if self.root is None:
            raise ValueError("Treap is empty")
        return self.root.forward_order()

    def __len__(self):
        """
        :return: number of nodes in tree
        """
        return len(self.root)
