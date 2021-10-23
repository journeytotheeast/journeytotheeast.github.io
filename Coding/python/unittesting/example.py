import requests

class Employee:
    """ A sample Employee class """

    raise_amt = 1.05

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)

    def monthly_schedule(self, month):
        response = requests.get(f'http://company.com/{self.last}/{month}')
        if response.ok:
            return response.text
        else:
            return 'Bad Response!'

def add(x, y):
    """ Add function """
    return x + y


def subtract(x, y):
    """ Subtract function """
    return x - y

def multiply(x, y):
    """ Multiply function """
    return x * y

def divide(x, y):
    """ Divide function """
    if y == 0:
        raise ValueError('Cannot divide by zero!')
    return x / y