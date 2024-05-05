import jwt
import logging


logger = logging.getLogger(__name__)


from code_manager.settings.base import env


def get_token(request) -> str:
    """Returns the JWT token from header"""

    token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[
        1
    ]  # split ["Bearer", 'token]
    return token


def decode_jwt(request) -> dict:
    """Decodes a JWT token and returns the payload as a dictionary.

    Args:
    token: The JWT token string.

    Returns:
    A dictionary containing the decoded payload or None if decoding fails.
    """

    try:
        token = get_token(request=request)
        jwt_signing_key = env("JWT_SIGNING_KEY")
        payload = jwt.decode(jwt=token, key=jwt_signing_key, algorithms=["HS256"])
        return payload  # payload has additional user details. see Auth Service's CustomTokenObtainPairSerializer
    except jwt.DecodeError:
        logger.warning("JWT signature verification failed")
        return None


def generate_submission_id() -> str:
    """Generates a UUID

    Args:
        None

    Return:
        A UUID4 string.
    """


if __name__ == "__main__":
    pass


# decode without jwt package (this way can not verify the signature)
"""
import base64
import json
# Assuming the token is in the token variable 
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwicGsiOiIxMDEiLCJjbGFzcyI6IlZJSUkiLCJzY2hvb2wiOiJwb3JpZGhpIiwiaWF0IjoxNTE2MjM5MDIyfQ.PBTrPfKnqDoAloaw8662vM6ajXhnjB2MwCkX3wZRKDs"
# Split by dot and get middle, payload, part;
token = token.split(".")
header, token_payload, signature = token[0], token[1], token[2]

token_payload_decoded = str(base64.b64decode(token_payload + "=="), "utf-8")

payload = json.loads(token_payload_decoded)

header_decoded = str(base64.b64decode(header+"=="), 'utf-8')
print(header_decoded)


name = payload["name"]

#############

# import base64
# import json

# def decode_jwt2(token: str):


#     # Assuming the token is in the token variable
#     token = (
#         "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIDIiLCJpYXQiOjE1MTYyMzkwMjJ9.3yw9-76uzuYlstomNB0mdb0ugEMSeicq8UMR34_UHW0"
#     )
#     # Split by dot and get middle, payload, part;
#     token_payload = token.split(".")[1]
#     # Payload is base64 encoded, let's decode it to plain string
#     # To make sure decoding will always work - we're adding max padding ("==")
#     # to payload - it will be ignored if not needed.
#     token_payload_decoded = str(base64.b64decode(token_payload + "=="), "utf-8")
#     # Payload is JSON - we can load it to dict for easy access
#     payload = json.loads(token_payload_decoded)
#     # And now we can access its' elements - e.g. name
#     name = payload["name"]
#     # Let's print it - it should show "John Doe"
#     print(name)
#     return payload

"""
