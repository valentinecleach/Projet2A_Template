from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt 
#from jwt import DecodeError, ExpiredSignatureError

from src.Webservice.init_app import jwt_service


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        # async = code asynchrone.
        # on peut faire attendre la fontion call pendant un moment
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(request)
       
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        try:
            jwt_service.validate_user_jwt(credentials.credentials)
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=403, detail="Expired token") from e
        except jwt.DecodeError as e:
            raise HTTPException(status_code=403, detail="Error decoding token") from e
        except Exception as e:
            raise HTTPException(status_code=403, detail="Unknown error") from e

        return credentials