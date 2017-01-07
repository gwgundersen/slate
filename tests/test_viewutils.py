"""Unit tests for viewutils modules.
"""

import unittest

from slate.models.user import User
from slate.models.expense import Expense
from slate.models.category import Category
from slate.endpoints import viewutils


class TestViewUtils(unittest.TestCase):

    def setUp(self):
        self.user = User('test', 'test')

    def test_get_category_sum(self):
        expense = [
            Expense(1, Category('food (out)'), '', True, self.user),
            Expense(2, Category('food (out)'), '', True, self.user),
            Expense(3, Category('alcohol'), '', True, self.user),
            Expense(4, Category('transportation (local)'), '', True,
                    self.user),
            Expense(5, Category('miscellaneous'), '', True, self.user)
        ]
        sum_ = viewutils.get_category_sum(expense)
        self.assertTrue(sum_ == 15)

    def tearDown(self):
        pass
