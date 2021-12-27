# -*- coding: UTF-8 -*-
"""
@Project : 3-PythonicTips 
@File    : survey_class.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 27/12/2021 02:56 
@Brief   : 
"""


class AnonymousSurvey:
    """Collect anonymous answers to a survey question."""

    def __init__(self, question):
        """Store a question, and prepare to store responses."""
        self.question = question
        self.responses = []

    def show_question(self):
        """Show the survey questions."""
        print(self.question)

    def store_response(self, new_response):
        """Store a single response to the survey."""
        self.responses.append(new_response)

    def show_results(self):
        """Show all the responses that have been given."""
        print("Survey results:")
        for response in self.responses:
            print(f"- {response}")