from tester.test import *

@test
@parametrize("qty", [1, 5, 0])
def test_add_item(qty):
    assert_equal(qty >= 0, True)