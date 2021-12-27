# -*- coding: UTF-8 -*-
"""
@Project : 3-PythonicTips 
@File    : name_function_testing.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 27/12/2021 02:45 
@Brief   : Test for a function
"""
import unittest

from name_function import get_formatted_name


""" 
In this test case, we only need to create a class to inherit `unittest.TestCase`, then we write the test function in 
this class and use `unittest.main()` in the main thread to finish this test file.  
"""


class NamesTestCase(unittest.TestCase):
    def test_first_last_name(self):
        formatted_name = get_formatted_name('andrew', 'yang')
        self.assertEqual(formatted_name, 'Andrew Yang')

    def test_first_last_middle_name(self):
        formatted_name = get_formatted_name('wolfgang', 'mozart', 'amadeus')
        self.assertEqual(formatted_name, 'Wolfgang Amadeus Mozart')


if __name__ == '__main__':
    unittest.main()

