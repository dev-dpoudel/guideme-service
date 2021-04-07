import unittest
import requests
import json


class TestPlaceClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.baseurl = "http://localhost:8000/place{}"

    def test_1_integrated_place(self):
        placename = "TestPlace"
        payload = {"name": placename,"country": "Nepal","city":"Pokhara"}
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
        self.assertEquals(data["name"], placename, "place Mismatch Error")
        url = self.baseurl.format("s")
        response = requests.post(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        self.assertGreaterEqual(len(data), 1, "No places returned")

        # Test Udate 
        data = {"tags": ['natural', 'scene', 'tourism']}  # noqa E501
        payload = json.dumps(data)
        url = self.baseurl.format("/" + id)
        response = requests.patch(url, data=payload)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)

        # Test Filter
        data = {"filterinfo": [
            {"field": "name", "expr": "eq", "combine": "and", "value": placename}]
            }

        # Set URL Parameters
        url = self.baseurl.format("s")
        response = requests.post(url, data=json.dumps(data))
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        if len(data) >= 1:
            product = data[0]
            self.assertEquals(product['name'], placename, "place Mismatch")
        
        #  Test delete Product
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
    suite.addTest(TestPlaceClass('test_1_integrated_place'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
