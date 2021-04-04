import unittest
import requests
import json


class TestPermissionClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.baseurl = "http://localhost:8000/group{}"

    def test_1_create_group(self):
        payload = {"name": "TestGroup", "permission": {"user": "list get put delete"}}
        data = json.dumps(payload)
        url = self.baseurl.format("/")
        response = requests.post(url, data=data)
        self.assertEquals(response.status_code, 200, response.text)

    def test_2_get_group(self):
        groupname = "TestGroup"
        url = self.baseurl.format('/' + groupname)
        response = requests.get(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        self.assertEquals(data["name"], groupname, "Group Mismatch Error")

    def test_3_list_group(self):
        url = self.baseurl.format("s")
        response = requests.post(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        self.assertGreaterEqual(len(data), 1, "No Groups returned")

    def test_40_update_group(self):
        data = {"name": "TestGroup", "permission": {"user": "list get put delete patch"}}  # noqa E501
        payload = json.dumps(data)
        url = self.baseurl.format("/")
        response = requests.patch(url, data=payload)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)


    def test_5_filter_group(self):

        # Set Filter Data
        data = {"filterinfo": [
            {"field": "name", "expr": "eq", "combine": "and", "value": "TestGroup"}            ]
            }

        # Set URL Parameters
        url = self.baseurl.format("s")
        response = requests.post(url, data=json.dumps(data))
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        if len(data) >= 1:
            group = data[0]
            self.assertEquals(group['name'], "TestGroup", "Group Mismatch")

    def test_6_query_group(self):

        # Set Filter Data
        data = {"filterinfo": [
            {"field": "name","expr": "eq","combine": "and","value": "TestGroup"},  # noqa E501
            {"field": "permission","expr": "eq","combine": "or","value": "Admin"}  # noqa E501
            ]
            }

        url = self.baseurl.format("s")
        response = requests.post(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, "Server response error")
        self.assertEquals(
            response.headers["Content-Type"], "application/json", "Invalid Output")  # noqa E501
        if len(data) >= 1:
            group = data[0]
            self.assertIn(group['name'], ['Admin', 'TestGroup'], "Group not in Requests")  # noqa E501

    def test_7_delete_group(self):
        groupname = "TestGroup"
        url = self.baseurl.format('/' + groupname)
        response = requests.delete(url)
        self.assertEquals(response.status_code, 200, response.text)


    def test_8_no_group(self):
        groupname = "TestGroup"
        url = self.baseurl.format("/" + groupname)
        response = requests.get(url)
        self.assertEquals(response.status_code, 404, response.text)

    def tearDown(self):
        del self.baseurl


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestUserClass('test_1_create_group'))
    suite.addTest(TestUserClass('test_2_list_group'))
    suite.addTest(TestUserClass('test_3_get_group'))
    suite.addTest(TestUserClass('test_40_update_group'))
    # suite.addTest(TestUserClass('test_41_set_group'))
    # suite.addTest(TestUserClass('test_42_unset_group'))
    suite.addTest(TestUserClass('test_5_filter_group'))
    suite.addTest(TestUserClass('test_6_query_group'))
    suite.addTest(TestUserClass('test_7_delete_group'))
    suite.addTest(TestUserClass('test_8_no_group'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
