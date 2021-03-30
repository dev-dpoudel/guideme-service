import unittest
from dependencies.filters import FilterModel, Filters
from mongoengine.queryset.visitor import Q


class TestFilteringClass(unittest.TestCase):

    def setUp(self):
        CFilters = []
        CFilters.append(FilterModel(field="username",
                                    value="alfaaz",
                                    expr="eq",
                                    combine="and"))

        # Filter Model
        CFilters.append(FilterModel(field="age",
                                    value=25,
                                    expr="eq",
                                    combine="and"))
        self.Filter = Filters(CFilters)

        CQuery = []
        CQuery.append(FilterModel(field="username",
                                  value="alfaaz",
                                  expr="eq",
                                  combine="and"))

        # Filter Model
        CQuery.append(FilterModel(field="age",
                                  value=25,
                                  expr="eq",
                                  combine="or"))

        self.Query = Filters(CQuery)

    def test_isType(self):
        self.assertEquals(self.Filter.get_filter_type(),
                          "Filters",
                          'Type mismatch for Filters')
        self.assertEquals(self.Query.get_filter_type(),
                          "Query",
                          'Type mismatch for Query Combination')

    def test_isValid(self):
        self.assertEquals(self.Filter.get_filters(),
                          {"username": "alfaaz", "age": 25},
                          'incorrect filters')

        self.assertEquals(self.Query.get_filters(),
                          Q(**{"username": "alfaaz"}) | Q(**{"age": 25}),
                          'incorrect queries')

    def test_isEmpty(self):
        self.Filter.reset_filter()
        self.assertIsNone(self.Filter.get_filters(), 'Nont None')

        self.Query.reset_filter()
        self.assertIsNone(self.Query.get_filters(), 'Nont None')

    def tearDown(self):
        del self.Query
        del self.Filter


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestFilteringClass('test_isValid'))
    suite.addTest(TestFilteringClass('test_filterType'))
    suite.addTest(TestFilteringClass('test_isEmpty'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
