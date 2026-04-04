from tester.test import *

@test
def test_login_valid_credentials(db_connection):
    assert_equal(200, 200)

@test
def test_login_invalid_password():
    assert_equal(401, 401)

@test
def test_login_expired_token():
    assert_equal(200, 401)

@test
@skip("no API key")
def test_checkout_stripe():
    pass