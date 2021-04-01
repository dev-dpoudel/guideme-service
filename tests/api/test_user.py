import unittest
import requests
import json


class TestUserClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.baseurl = "http://localhost:8000/user/{}"

    def test_1_create_users(self):
        payload = {"username": "invaliduser", "password": "invalidpass"}
        url = self.baseurl.format("create")
        response = requests.post(url, data=payload)
        self.assertEquals(response.status_code, 200, response.text)

    def test_2_get_user(self):
        username = "invaliduser"
        url = self.baseurl.format(username)
        response = requests.get(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        self.assertEquals(data["username"], username, "User Mismatch Error")

    def test_3_list_users(self):
        url = self.baseurl.format("")
        response = requests.post(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        self.assertGreaterEqual(len(data), 1, "No user returned")

    def test_40_update_users(self):
        data = {"username": "invaliduser", "first_name": "Invalid", "last_name":"User", "is_active": "False"}  # noqa E501
        payload = json.dumps(data)
        url = self.baseurl.format("update")
        response = requests.patch(url, data=payload)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)


    # def test_41_set_users(self):
    #     group = {"groups": ["users", "groups"]}
    #     payload = json.dumps(group)
    #     url = self.baseurl.format("invaliduser/group/add")
    #     response = requests.patch(url, data=payload)
    #     data = response.json()
    #     self.assertEquals(response.status_code, 200, response.text)
    #     self.assertEquals(data["group"], group, response.text)

    # def test_42_unset_users(self):
    #     group = {"groups": ["users", "groups"]}
    #     payload = json.dumps(group)
    #     url = self.baseurl.format("invaliduser/group/remove")
    #     response = requests.patch(url, data=payload)
    #     data = response.json()
    #     self.assertEquals(response.status_code, 200, response.text)
    #     self.assertEquals(data["group"], None, response.text)

    def test_5_filter_users(self):

        # Set Filter Data
        data = {"filterinfo": [
            {"field": "city", "expr": "eq", "combine": "and", "value": ""},
            {"field": "is_active", "expr": "eq", "combine": "and", "value": False}  # noqa E501
            ]
            }

        # Set URL Parameters
        url = self.baseurl.format("")
        response = requests.post(url, data=json.dumps(data))
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        if len(data) >= 1:
            user = data[0]
            self.assertEquals(user['city'], "", "City Mismatch")
            self.assertEquals(user['isActive'], False, "User Status Mismatch")

    def test_6_query_users(self):

        # Set Filter Data
        data = {"filterinfo": [
            {"field": "username","expr": "eq","combine": "and","value": "invaliduser"},  # noqa E501
            {"field": "username","expr": "eq","combine": "or","value": "alfaaz"}  # noqa E501
            ]
            }

        url = self.baseurl.format("")
        response = requests.post(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, "Server response error")
        self.assertEquals(
            response.headers["Content-Type"], "application/json", "Invalid Output")  # noqa E501
        if len(data) >= 1:
            user = data[0]
            self.assertIn(user['username'], ['alfaaz', 'invaliduser'], "User not in Requests")  # noqa E501

    def test_7_delete_users(self):
        url = self.baseurl.format("invaliduser")
        response = requests.delete(url)
        self.assertEquals(response.status_code, 200, response.text)


    def test_8_no_user(self):
        username = "invaliduser"
        url = self.baseurl.format(username)
        response = requests.get(url)
        self.assertEquals(response.status_code, 404, response.text)

    def tearDown(self):
        del self.baseurl


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestUserClass('test_1_create_users'))
    suite.addTest(TestUserClass('test_2_list_users'))
    suite.addTest(TestUserClass('test_3_get_user'))
    suite.addTest(TestUserClass('test_40_update_users'))
    # suite.addTest(TestUserClass('test_41_set_group'))
    # suite.addTest(TestUserClass('test_42_unset_group'))
    suite.addTest(TestUserClass('test_5_filter_users'))
    suite.addTest(TestUserClass('test_6_query_users'))
    suite.addTest(TestUserClass('test_7_delete_users'))
    suite.addTest(TestUserClass('test_8_no_user'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
