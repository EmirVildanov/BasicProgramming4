from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Iterator, TypeVar, Generic, Optional

K = TypeVar("K")
V = TypeVar("V")


@dataclass()
class Node(Generic[K, V]):
    key: K
    priority: V
    left_child: Optional[Node[K, V]] = None
    right_child: Optional[Node[K, V]] = None

    def __len__(self):
        left_child_len = 0
        right_child_len = 0
        if self.left_child is not None:
            left_child_len = len(self.left_child)
        if self.right_child is not None:
            right_child_len = len(self.right_child)
        return 1 + left_child_len + right_child_len

    def __iter__(self):
        return self.forward_order()

    def backward_order(self) -> Iterator[Tuple[K, V]]:
        if self.right_child is not None:
            yield from self.right_child.backward_order()
        yield self.key, self.priority
        if self.left_child is not None:
            yield from self.left_child.backward_order()

    def forward_order(self) -> Iterator[Tuple[K, V]]:
        if self.left_child is not None:
            yield from self.left_child.forward_order()
        yield self.key, self.priority
        if self.right_child is not None:
            yield from self.right_child.forward_order()

    def split(self, key: K) -> Tuple[Optional[Node[K, V]], Optional[Node[K, V]]]:
        if key > self.key:
            if self.right_child is None:
                return Node(self.key, self.priority, self.left_child, None), None
            smaller_tree_node, bigger_tree_node = self.right_child.split(key)
            return Node(self.key, self.priority, self.left_child, smaller_tree_node), bigger_tree_node
        if self.left_child is None:
            return None, Node(self.key, self.priority, None, self.right_child)
        smaller_tree_node, bigger_tree_node = self.left_child.split(key)
        return smaller_tree_node, Node(self.key, self.priority, bigger_tree_node, self.right_child)

    def merge(self, other: Optional[Node[K, V]]) -> Node[K, V]:
        if other is None:
            return self
        self_max_key, _ = next(self.forward_order())
        other_min_key, _ = next(other.backward_order())
        if self_max_key >= other_min_key:
            raise ValueError("Every key from merging treap should be bigger than every key from current treap")
        if self.priority > other.priority:
            if self.right_child is None:
                return Node(self.key, self.priority, self.left_child, other)
            return Node(self.key, self.priority, self.left_child, self.right_child.merge(other))
        return Node(other.key, other.priority, self.merge(other.left_child), other.right_child)

    def __contains__(self, key: K):
        if self.key == key:
            return True
        elif self.key < key:
            if self.right_child is None:
                return False
            return key in self.right_child
        if self.left_child is None:
            return key in self.left_child

    def __getitem__(self, key: K):
        if self.key == key:
            return self.priority
        elif self.key < key:
            if self.right_child is None:
                raise KeyError(f"Treap does not contain key {key}")
            return self.right_child[key]
        if self.left_child is None:
            raise KeyError(f"Treap does not contain key {key}")
        return self.left_child[key]

    def insert(self, key: K, priority: V) -> Node[K, V]:
        smaller_tree_node, bigger_tree_node = self.split(key)
        if smaller_tree_node is None:
            smaller_tree_node = Node(key, priority)
        return smaller_tree_node.merge(Node(key, priority, None, None)).merge(bigger_tree_node)

    def remove(self, key: K) -> Node[K, V]:
        if key not in self:
            raise KeyError(f"Treap does not contain key {key}")
        smaller_tree_node, bigger_tree_node = self.split(key)

        # Algorithm says it is impossible
        if bigger_tree_node is None:
            raise ValueError("Got None right tree after splitting")

        if smaller_tree_node is None:
            return bigger_tree_node.get_without_smallest_key()
        return smaller_tree_node.merge(bigger_tree_node.get_without_smallest_key())

    def get_without_smallest_key(self) -> Optional[Node[K, V]]:
        if self.left_child is None:
            return self.right_child
        return Node(self.key, self.priority, self.left_child.get_without_smallest_key(), self.right_child)
