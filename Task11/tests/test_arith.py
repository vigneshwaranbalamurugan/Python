from tester.test import *

@test
def test_addition():
    assert_equal(2 + 3, 7)

@test
def test_subtraction():
    assert_equal(5 - 2, 3)

@test
def test_multiplication():
    assert_equal(4 * 3, 15)

@test
def test_division():
    assert_equal(10 / 2, 5)
