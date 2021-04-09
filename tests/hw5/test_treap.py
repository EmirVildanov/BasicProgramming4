import unittest

from homework.hw5.treap import Treap


class SmartArgsTestCase(unittest.TestCase):
    def test_should_raise_exception(self):
        with self.assertRaises(ValueError) as context:
            ...

        self.assertTrue("" in str(context.exception))

    def test_should_test(self):
        val1 = 1
        val2 = 2

        self.assertTrue(val1 < val2)

    def test_should_test_treap_work_correctly(self):
        treap = Treap()
        treap["a"] = 1
        treap["b"] = 2
        treap["c"] = 4
        treap["d"] = -1
        treap["e"] = 3
        print(treap.root)

    def test_should_test_treap_work_correctly_again(self):
        treap = Treap()
        treap["a"] = 3
        treap["b"] = 4
        treap["c"] = 6
        treap["d"] = 1
        treap["e"] = 5
        print(treap.root)

