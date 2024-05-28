# python
import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError, InvalidTokenError, ExpiredSignatureError
import logging

# django
from django.conf import settings

logger = logging.getLogger(__name__)


# an example jwt claim/payload
"""
{'token_type': 'access', 'exp': 1715259702, 'iat': 1714827702, 
'jti': '39cc1a60e865449da642dcf0cafdad09', 
'user_id': 'a0099fea-455b-409b-87d5-633dde71dca3', 
'first_name': 'Kemal', 'last_name': 'Soydere', 'username': 'kemal_1', 
'email': 'kemal1@gmail.com'} 
"""


class DecodeJWT:
    """Decode JWT Util Class"""

    def get_token(self, request) -> str:
        """Returns the JWT token from header"""

        auth_header = request.META.get("HTTP_AUTHORIZATION", None)  

        if auth_header is None: 
            return None 
        parts = auth_header.split(" ")  # parts ["Bearer", 'token]
        if len(parts) != 2 or parts[0].lower() != "bearer": 
            return None 
        return parts[1]

    def decode_jwt(self, request) -> dict:
        """Decodes a JWT token and returns the payload as a dictionary.
        Args:
        token: The JWT token string.
        Returns:
        A dictionary containing the decoded payload or None if decoding fails.
        """
        try:
            token = self.get_token(request=request)

            if token is None: 
                logger.error(f"\n[JWT ERROR]: Token is missing or malformed Authorization header.")
                return None, "jwt-header-malformed"            
            jwt_signing_key = settings.JWT_SIGNING_KEY
            payload = jwt.decode(jwt=token, key=jwt_signing_key, algorithms=["HS256"])
            return payload  # payload has additional user details. see Auth Service's CustomTokenObtainPairSerializer
        except ExpiredSignatureError as e: 
            logger.error(f"\n[JWT ERROR]: JWT signature is Expired.\n[EXCEPTION]: {str(e)}")
            return None, "jwt-signature-expired"
        except (DecodeError, InvalidSignatureError, InvalidTokenError) as e:
            logger.error(f"\n[JWT ERROR]: JWT signature verification failed.\n[EXCEPTION]: {str(e)}")
            return None, "jwt-decode-error"


# instance to call
jwt_decoder = DecodeJWT()
