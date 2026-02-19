from jose import jwt, JWTError, ExpiredSignatureError
from decouple import config
from datetime import timedelta, timezone, datetime

from src.modules.users.models import UserModel

from src.shared.exceptions import UnauthorizedException


class JwtService:
    def __init__(self):
        self._secret_key = config("SECRET_KEY")
        self._algorithm = "HS256"
        self._issuer = config("JWT_ISSUER")
        self._audience = config("JWT_AUDIENCE")

    def _create_token(self, model: UserModel, expires_minutes: int, scope: str = "access_token") -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

        payload = {
            "sub": str(model.uuid),
            "iss": self._issuer,
            "aud": self._audience,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "scope": scope
        }

        if scope == "access_token":
            payload["username"] = model.username
            payload["is_staff"] = model.is_staff

        return jwt.encode(payload, self._secret_key, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                audience=self._audience,
                issuer=self._issuer,
                options={"require": ["exp", "iss", "aud", "sub"]}
            )
            return payload

        except ExpiredSignatureError:
            raise UnauthorizedException("Token has expired")
        
        except JWTError as e:
            raise UnauthorizedException("Invalid token")
            
        except Exception:
            raise UnauthorizedException("Could not validate credentials")