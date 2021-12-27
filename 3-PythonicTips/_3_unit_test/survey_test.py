# -*- coding: UTF-8 -*-
"""
@Project : 3-PythonicTips 
@File    : survey_test.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 27/12/2021 02:58 
@Brief   : 
"""
import unittest

from survey_class import AnonymousSurvey


class TestAnonymousSurvey(unittest.TestCase):
    """Tests for the class AnonymousSurvey."""

    def test_store_single_response(self):
        """Test that a single response is stored properly."""
        question = "What language did you first learn to speak?"
        my_survey = AnonymousSurvey(question)
        my_survey.store_response('English')
        self.assertIn('English', my_survey.responses)

    def test_store_three_responses(self):
        question = "What language did you first learn to speak?"
        my_survey = AnonymousSurvey(question)
        responses = ['English', 'Chinese', 'Spanish']
        for response in responses:
            my_survey.store_response(response)
        self.assertIn('English', my_survey.responses)


class TestAnonymousSurvey2(unittest.TestCase):

    def setUp(self):
        question = "What language did you first learn to speak?"
        self.my_survey = AnonymousSurvey(question)
        self.responses = ['Fuzhounese', 'Chinese', 'English']

    def test_store_single_response(self):
        question = "What language did you first learn to speak?"
        self.my_survey.store_response(self.responses[0])
        self.assertIn('Fuzhounese', self.my_survey.responses)

    def test_store_responses(self):
        question = "What language did you first learn to speak?"
        for response in self.responses:
            self.my_survey.store_response(response)
        for response in self.responses:
            self.assertIn(response, self.my_survey.responses)


if __name__ == '__main__':
    unittest.main()

