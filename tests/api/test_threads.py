import unittest
import requests
import json


class TestRatingsClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.baseurl = "http://localhost:8000/rating{}"

    def test_1_integrated_ratings(self):
        ratingsname = "60670e19c94660663f15f3b9"
        payload = {"thread": ratingsname,"rating": 4, "review": "User Group is lazy and tedious"}
        data = json.dumps(payload)
        url = self.baseurl.format("/")
        response = requests.post(url, data=data)
        data = response.json()
        id = data['id']
        self.assertEquals(response.status_code, 200, response.text)

        # Test Get Request
        url = self.baseurl.format('/' + id)
        response = requests.get(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)

        # Test List Requests
        self.assertEquals(data["thread"], ratingsname, "Thread Mismatch Error")
        url = self.baseurl.format("s")
        response = requests.post(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        self.assertGreaterEqual(len(data), 1, "No ratings returned")

        # Test Udate 
        data = {"review": "Empty Description"}  # noqa E501
        payload = json.dumps(data)
        url = self.baseurl.format("/" + id)
        response = requests.patch(url, data=payload)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)

        # Test Filter
        data = {"filterinfo": [
            {"field": "thread", "expr": "eq", "combine": "and", "value": ratingsname}]
            }

        # Set URL Parameters
        url = self.baseurl.format("s")
        response = requests.post(url, data=json.dumps(data))
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        if len(data) >= 1:
            ratings = data[0]
            self.assertEquals(ratings['thread'], ratingsname, "Thread Mismatch")
        
        #  Test delete ratings
        url = self.baseurl.format('/' + id)
        response = requests.delete(url)
        self.assertEquals(response.status_code, 200, response.text)

        # Test No Data
        url = self.baseurl.format("/" + id)
        response = requests.get(url)
        self.assertEquals(response.status_code, 404, response.text)


    def tearDown(self):
        del self.baseurl


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestRatingsClass('test_1_integrated_ratings'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
