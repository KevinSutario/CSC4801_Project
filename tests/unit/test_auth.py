"""Auth requirement tests (FP-AUTH-*, FP-SEC-2). Placeholders owned by T04; T05 and
T06 replace them with real tests (T06 owns test_fp_auth_3_authorization_and_missing_object)."""

import pytest


@pytest.mark.skip(reason="TODO T05")
def test_fp_auth_1_registration_and_session_lifecycle():
    raise NotImplementedError


@pytest.mark.skip(reason="TODO T05")
def test_fp_auth_1_invalid_registration():
    raise NotImplementedError


@pytest.mark.skip(reason="TODO T05")
def test_fp_auth_2_salted_hash_and_password_verification():
    raise NotImplementedError


@pytest.mark.skip(reason="TODO T06")
def test_fp_auth_3_authorization_and_missing_object():
    raise NotImplementedError


@pytest.mark.skip(reason="TODO T05")
def test_fp_sec_2_sql_metacharacters_stay_bound():
    raise NotImplementedError
