import unittest
import requests
import json


class TestProductClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.baseurl = "http://localhost:8000/product{}"

    def test_1_integrated_product(self):
        productname = "TestProduct"
        payload = {"name": productname,"identity": "Test W093"}
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
        self.assertEquals(data["name"], productname, "product Mismatch Error")
        url = self.baseurl.format("s")
        response = requests.post(url)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        self.assertGreaterEqual(len(data), 1, "No products returned")

        # Test Udate 
        data = {"tags": ['noodles', 'nepali', 'foods']}  # noqa E501
        payload = json.dumps(data)
        url = self.baseurl.format("/" + id)
        response = requests.patch(url, data=payload)
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)

        # Test Filter
        data = {"filterinfo": [
            {"field": "name", "expr": "eq", "combine": "and", "value": productname}]
            }

        # Set URL Parameters
        url = self.baseurl.format("s")
        response = requests.post(url, data=json.dumps(data))
        data = response.json()
        self.assertEquals(response.status_code, 200, response.text)
        if len(data) >= 1:
            product = data[0]
            self.assertEquals(product['name'], productname, "product Mismatch")
        
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
    suite.addTest(TestProductClass('test_1_integrated_product'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
