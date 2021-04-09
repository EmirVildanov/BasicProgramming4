import unittest

from homework.hw5.treap import Treap


class SmartArgsTestCase(unittest.TestCase):
    def test_should_raise_exception_when_Evaluated_gets_Isolated_as_argument(self):
        with self.assertRaises(ValueError) as context:
            ...

        self.assertTrue("Isolated argument is not supported by Evaluated" in str(context.exception))

    def test_should_test_Evaluated_works_properly_with_date_function(self):
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

