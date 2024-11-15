import time

# pip install pyjwt
import jwt
import pytest
from jwt import ExpiredSignatureError

from src.Model.jwt_response import JWTResponse
from src.Service.jwt_service import JwtService


@pytest.fixture
def jwt_service():
    """Fixture qui fournit une instance de JwtService avec une clé secrète pour les tests."""
    return JwtService(secret="my_secret_key")


@pytest.fixture
def valid_token(jwt_service):
    """Fixture qui fournit un token JWT valide pour les tests."""
    return jwt_service.encode_jwt(user_id=1).access_token


def test_encode_jwt(jwt_service):
    """Test de la génération d'un JWT."""
    response = jwt_service.encode_jwt(user_id=123)

    assert isinstance(response, JWTResponse)
    assert isinstance(response.access_token, str)

    decoded = jwt.decode(
        response.access_token, jwt_service.secret, algorithms=[jwt_service.algorithm]
    )
    assert decoded["user_id"] == 123
    assert decoded["expiry_timestamp"] > time.time()


def test_decode_jwt(jwt_service, valid_token):
    """Test du décodage d'un JWT valide."""
    decoded = jwt_service.decode_jwt(valid_token)

    assert decoded["user_id"] == 1
    assert decoded["expiry_timestamp"] > time.time()


def test_validate_user_jwt_valid(jwt_service, valid_token):
    """Test de validation d'un JWT valide."""
    user_id = jwt_service.validate_user_jwt(valid_token)

    assert user_id == 1


def test_validate_user_jwt_expired(jwt_service):
    """Test de validation d'un JWT expiré."""
    expired_payload = {"user_id": 1, "expiry_timestamp": time.time() - 10}
    expired_token = jwt.encode(
        expired_payload, jwt_service.secret, algorithm=jwt_service.algorithm
    )

    with pytest.raises(ExpiredSignatureError):
        jwt_service.validate_user_jwt(expired_token)


def test_invalid_jwt(jwt_service):
    """Test d'un JWT invalide."""
    invalid_token = "invalid_token"

    with pytest.raises(jwt.exceptions.DecodeError):
        jwt_service.decode_jwt(invalid_token)


def test_validate_user_jwt_with_invalid_signature(jwt_service):
    """Test d'un JWT avec une signature incorrecte."""
    token_with_invalid_signature = jwt.encode(
        {"user_id": 1, "expiry_timestamp": time.time() + 600},
        "wrong_secret",
        algorithm="HS256",
    )

    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        jwt_service.decode_jwt(token_with_invalid_signature)
