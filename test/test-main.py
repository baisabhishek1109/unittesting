import unittest
from io import StringIO
from unittest import TestCase
from mock import patch
import sys, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from testlib import tag


# using global varibale to share data
input_data = "Hello World"

def setUpModule():
    print "in setUpModule"

def tearDownModule():
    print "\nin tearDownModule"

class TestContainer(TestCase):
    global input_data

    @classmethod
    def setUpClass(cls):
        print "in setUpClass"

    @classmethod
    def tearDownClass(cls):
        print "\nin tearDownClass"

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    @tag("string")
    def test_strings(self):
        print('inside data')
        self.assertTrue("HII".isupper())

    @tag("string")
    def test_spliting(self):
        print('inside data')
        with self.assertRaises(AttributeError):
            input_data.split(2)

    def test_stdout(self):
        print('inside data')
        with patch('sys.stdout',new=StringIO()) as fake_output:
            sys.stdout.write(u"hello world\n")
            result = fake_output
            self.assertEqual(result.getvalue(),"hello world\n")

    def test_selenium(self):
        print('inside data')
        self.driver.get("http://www.python.org")
        assert "Python" in self.driver.title
        elem = self.driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        self.assertTrue("No results found." not in self.driver.page_source)

    def tearDown(self):
        self.driver.close()



# log inot file
def main(out=sys.stderr,verbosity=2):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out,verbosity=verbosity).run(suite)


if __name__ == '__main__':
    input_data = None
    with open('test_output.out','w') as f:
        main(f)