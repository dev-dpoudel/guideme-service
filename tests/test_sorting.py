import unittest
from dependencies.sorting import SortingModel, Sorters
from fastapi import HTTPException


class TestSortingClass(unittest.TestCase):

    CSorters = []
    CSorters.append(SortingModel(field="username", type="asc"))
    CSorters.append(SortingModel(field="country", type="desc"))

    def setUp(self):
        self.Sorter = Sorters(self.CSorters)

    def test_isValid(self):
        result = ['+username','-country']
        self.assertEqual(self.Sorter.get_order_by(),result,'incorrect sorting')

    def test_raisesHttpException(self):
        self.assertRaises(HTTPException)

    def test_isEmpty(self):
        self.Sorter.reset_sorter()
        self.assertIsNone(self.Sorter.get_order_by(),'Nont None')

    def tearDown(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSortingClass('test_isValid'))
    suite.addTest(TestSortingClass('test_isEmpty'))
    suite.addTest(TestSortingClass('test_raisesHttpException'))
    return suite

if __name__ == '__main__':
    # runner = unittest.TextTestRunner()
    # runner.run(suite())
    unittest.main()