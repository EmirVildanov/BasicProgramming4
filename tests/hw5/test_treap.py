import unittest

from homework.hw5.treap import Treap
from homework.hw5.node import Node
from tests.utils import extract_message_string_from_context


class SmartArgsTestCase(unittest.TestCase):
    def test_should_raise_error_when_adding_instance_with_already_existed_key(self):
        key = 1

        with self.assertRaises(ValueError) as context:
            treap = Treap()
            treap[key] = 1
            treap[key] = 3

        self.assertTrue(f"Treap already contains key {key}" in extract_message_string_from_context(context))

    def test_should_raise_error_when_adding_instance_with_already_existed_priority(self):
        priority = 1

        with self.assertRaises(ValueError) as context:
            treap = Treap()
            treap[1] = priority
            treap[3] = priority

        self.assertTrue(f"Treap already contains priority {priority}" in extract_message_string_from_context(context))

    def test_should_raise_error_when_getting_instance_that_key_not_it_the_Treap(self):
        key = 5
        with self.assertRaises(KeyError) as context:
            treap = Treap()
            treap[1] = 5
            treap[3] = 7
            treap[key]

        self.assertTrue(f"Treap does not contain key {key}" in extract_message_string_from_context(context))

    def test_should_raise_error_when_getting_instance_when_treap_is_empty(self):
        key = 5
        with self.assertRaises(KeyError) as context:
            treap = Treap()
            treap[key]

        self.assertTrue(f"Treap does not contain key {key}" in extract_message_string_from_context(context))

    def test_should_raise_error_when_removing_instance_that_key_not_in_the_treap(self):
        key = 5
        with self.assertRaises(KeyError) as context:
            treap = Treap()
            treap[4] = 3
            treap.__delitem__(key)

        self.assertTrue(f"Treap does not contain key {key}" in extract_message_string_from_context(context))

    def test_should_raise_error_when_merging_treap_with_smaller_keys(self):
        with self.assertRaises(ValueError) as context:
            node1 = Node(6, 3)
            node2 = Node(3, 5)
            node1.merge(node2)

        self.assertTrue(
            "Every key from merging treap should be bigger than every key from current treap"
            in extract_message_string_from_context(context)
        )

    def test_should_return_len_of_treap(self):
        treap = Treap()
        treap[1] = 6
        treap[2] = 3
        treap[3] = 2
        treap[4] = 5
        treap[5] = 7
        self.assertTrue(5, len(treap))

    def test_should_check_treap_setitem_function_works_properly(self):
        treap = Treap()
        treap[1] = 1
        self.assertTrue(1 in treap.keys)

    def test_should_check_treap_contains_function_works_properly(self):
        treap = Treap()
        treap[1] = 1
        self.assertTrue(1 in treap)

    def test_should_check_treap_getitem_function_works_properly(self):
        test_priority = "test"
        treap = Treap()
        treap[1] = test_priority
        self.assertEqual(test_priority, treap[1])

    def test_should_check_treap_delitem_function_works_properly(self):
        test_key = "test"
        treap = Treap()
        treap[test_key] = 1
        self.assertTrue(treap.__contains__(test_key))
        treap.__delitem__(test_key)
        self.assertFalse(treap.__contains__(test_key))

    def test_should_check_treap_forward_iterator_works_properly2(self):
        treap = Treap()
        treap[1] = 5
        treap[5] = 4
        treap[3] = 3
        treap[10] = 2
        treap[2] = 1
        asserting_array = [(1, 5), (2, 1), (3, 3), (5, 4), (10, 2)]
        self.assertEqual(asserting_array, [*treap.forward_iterator()])

    def test_should_check_treap_backward_iterator_works_properly(self):
        treap = Treap()
        treap["a"] = 1
        treap["b"] = 2
        treap["c"] = 3
        treap["d"] = 4
        treap["e"] = 5
        asserting_array = [("e", 5), ("d", 4), ("c", 3), ("b", 2), ("a", 1)]
        self.assertEqual(asserting_array, [*treap.backward_iterator()])

    def test_should_check_treap_binary_tree_structure_works(self):
        def assert_binary_tree_structure(node: Node):
            if node.left_child is not None:
                assert_binary_tree_structure(node.left_child)
                self.assertTrue(node.key > node.left_child.key)
            if node.right_child is not None:
                self.assertTrue(node.key < node.right_child.key)
                assert_binary_tree_structure(node.right_child)

        treap = Treap()
        treap[1] = 3
        treap[5] = 32
        treap[6] = 7
        treap[55] = 23
        treap[3] = 9
        treap[47] = 11
        treap[17] = 300
        treap[90] = 90
        assert_binary_tree_structure(treap.root)
