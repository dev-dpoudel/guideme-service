import unittest
import requests
import json


class TestCommentsClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.baseurl = "http://localhost:8000/comment{}"

    def test_1_integrated_comments(self):
        threadname = "606d4793050af336956d49bd"
        payload = {"thread": threadname, "comment": "User Group Comment"}
        data = json.dumps(payload)
        url = self.baseurl.format("/")
        response = requests.post(url, data=data)
        print(response.content)
        data = response.json()
        print(data)
        id = data['id']
        self.assertEquals(response.status_code, 200, response.text)

        # Test Get Request
        url = self.baseurl.format('/' + id)
        response = requests.get(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)

        # Test List Requests
        url = self.baseurl.format("s")
        response = requests.post(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        self.assertGreaterEqual(len(data), 1, "No comments returned")

        # Test Udate 
        data = {"comment": "User Group Comment"}  # noqa E501
        payload = json.dumps(data)
        url = self.baseurl.format("/" + id)
        response = requests.patch(url, data=payload)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)

        # Test Filter
        data = {"filterinfo": [
            {"field": "thread", "expr": "eq", "combine": "and", "value": commentsname}]
            }

        # Set URL Parameters
        url = self.baseurl.format("s")
        response = requests.post(url, data=json.dumps(data))
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        if len(data) >= 1:
            comments = data[0]
            self.assertEquals(comments['thread'], commentsname, "Thread Mismatch")
        
        #  Test delete comments
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
    suite.addTest(TestCommentsClass('test_1_integrated_comments'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
