# -*- coding: UTF-8 -*-
"""
@Project : 3-PythonicTips 
@File    : _2_classmethod.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 25/12/2021 12:12 
@Brief   : Using classmethod means that you can use different constructor function to create the instance.
"""

from datetime import date


# random Person
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @staticmethod
    def fromFathersAge(name, fatherAge, fatherPersonAgeDiff):
        # the instance created by this method in the child class is the instance of `Person`, while not `man`.
        # Obviously, this kind of design method violates the OOP paradigm. Thus using `classmethod` is a good choice
        # to generate a new instance, like overloadding the constructor method in C++.
        return Person(name, date.today().year - fatherAge + fatherPersonAgeDiff)

    @classmethod
    def fromBirthYear(cls, name, birthYear):
        return cls(name, date.today().year - birthYear)

    def display(self):
        print(self.name + "'s age is: " + str(self.age))


class Man(Person):
    sex = 'Male'


if __name__ == '__main__':
    man = Man.fromBirthYear('John', 1985)
    print(isinstance(man, Man))

    man1 = Man.fromFathersAge('John', 1965, 20)
    print(isinstance(man1, Man))
