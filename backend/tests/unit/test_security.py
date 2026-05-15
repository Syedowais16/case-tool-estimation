"""Unit tests for authentication"""
import pytest
from app.core.security.security import (
    verify_password, get_password_hash, create_access_token,
    decode_token
)


def test_password_hashing():
    """Test password hashing"""
    plain_password = "test_password123"
    hashed = get_password_hash(plain_password)
    
    assert hashed != plain_password
    assert verify_password(plain_password, hashed)


def test_password_verification_fails_with_wrong_password():
    """Test password verification fails with wrong password"""
    plain_password = "test_password123"
    wrong_password = "wrong_password"
    hashed = get_password_hash(plain_password)
    
    assert not verify_password(wrong_password, hashed)


def test_create_access_token():
    """Test access token creation"""
    data = {"sub": "user123"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)


def test_decode_token():
    """Test token decoding"""
    data = {"sub": "user123"}
    token = create_access_token(data)
    payload = decode_token(token)
    
    assert payload.get("sub") == "user123"


def test_decode_invalid_token():
    """Test decoding invalid token"""
    from fastapi import HTTPException
    
    with pytest.raises(HTTPException):
        decode_token("invalid_token_here")
