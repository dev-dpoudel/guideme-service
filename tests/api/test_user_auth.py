import unittest
import requests


class TestAuthUserClass(unittest.TestCase):

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

    def test_3_get_me(self):
        url = self.baseurl.format("me")
        response = requests.get(url)
        print(response.content)
        self.assertEquals(response.status_code, 401, response.text)

    def test_4_auth_users(self):
        payload = {"grant_type": "password",
                   "username": "invaliduser",
                   "password": "invalidpass"}

        url = self.baseurl.format("token")
        response = requests.post(url, data=payload)
        self.assertEquals(response.status_code, 200, response.text)

        # Test for authorization success
        data = response.json()
        authorization = "{} {}".format(data['token_type'], data['access_token'])  # noqa E501
        headers = {'Authorization': authorization}
        url = self.baseurl.format("me")
        response = requests.get(url, headers=headers)
        self.assertEquals(response.status_code, 200, response.text)

    def test_7_delete_users(self):
        url = self.baseurl.format("invaliduser")
        response = requests.delete(url)
        self.assertEquals(response.status_code, 200, response.text)

    def tearDown(self):
        del self.baseurl


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAuthUserClass('test_1_create_users'))
    suite.addTest(TestAuthUserClass('test_2_get_user'))
    suite.addTest(TestAuthUserClass('test_3_auth_users'))
    suite.addTest(TestAuthUserClass('test_4_get_me'))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
