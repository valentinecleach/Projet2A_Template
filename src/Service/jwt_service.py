

# JSON Web tokens.

# Allows to decode, verify and generate JWT
import os
import time

# "pip install jwt" a ne pas oublier avant
# et "pip install --upgrade PyJWT"
import jwt

# Model
from src.Model.jwt_response import JWTResponse

#from jwt.exceptions import ExpiredSignatureError



class JwtService:
    """
    Handler for JWT encryption and validation
    """

    def __init__(self, secret: str = "", algorithm: str = "HS256"):
        """Creator
        """
        if secret == "":
            self.secret = os.environ["JWT_SECRET"]
        else:
            self.secret = secret
        self.algorithm = algorithm

    def encode_jwt(self, user_id: int) -> JWTResponse:
        """
        Creates a token with a 10 minutes expiry time
        """
        payload = {"user_id": user_id, "expiry_timestamp": time.time() + 600}
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return JWTResponse(access_token=token)

    def decode_jwt(self, token: str) -> dict:
        """
        Reads an authentication token
        """
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])

    def validate_user_jwt(self, token: str) -> str:
        """
        Returns the id of the user authenticated by the JWT
        Throws in case of invalid or expired JWT
        """
        decoded_jwt = self.decode_jwt(token)
        if decoded_jwt["expiry_timestamp"] < time.time():
            raise jwt.ExpiredSignatureError("Expired JWT")
        return decoded_jwt["user_id"]
