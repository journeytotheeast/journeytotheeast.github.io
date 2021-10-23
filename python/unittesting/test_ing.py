import unittest
from unittest.mock import patch
import example
from example import Employee


class TestEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')
        self.emp_1 = Employee('Roma', 'No', 1000)

    def tearDown(self):
        print('tearDown')

    def test_email(self):

        self.assertEqual(self.emp_1.email, 'Roma.No@email.com')

        self.emp_1.first = 'John'

        self.assertEqual(self.emp_1.email, 'John.No@email.com')

    def test_fullname(self):
        self.assertEqual(self.emp_1.fullname, 'Roma No')

        self.emp_1.first = 'Jane'

        self.assertEqual(self.emp_1.fullname, 'Jane No')

    def test_apply_raise(self):
        self.emp_1.apply_raise()

        self.assertEqual(self.emp_1.pay, 1000*1.05)

    def test_monthly_schedule(self):
        with patch('example.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            schedule = self.emp_1.monthly_schedule('May')
            mocked_get.assert_called_with('http://company.com/No/May')
            self.assertEqual(schedule, 'Success')

class TestCalc(unittest.TestCase):

    def test_add(self):
        result = example.add(10, 5)
        self.assertEqual(result, 15)

    def test_sub(self):
        self.assertEqual(example.subtract(10, 5), 5)

    def test_mul(self):
        self.assertEqual(example.multiply(10, 5), 50)

    def test_div(self):
        self.assertRaises(ValueError, example.divide, 10, 0)
        with self.assertRaises(ValueError):
            example.divide(0, 0)


if __name__ == '__main__':
    unittest.main()