# python
import jwt
import logging
import uuid
import time
from os import getpid
import hashlib
import random

# django
from django.core.exceptions import ValidationError
from django.conf import settings

# other
import boto3
from boto3.exceptions import S3TransferFailedError, S3UploadFailedError

# local
from code_manager.settings.base import env
from core_apps.code_display.models import Questions


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

        token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[
            1
        ]  # split ["Bearer", 'token]
        return token

    def decode_jwt(self, request) -> dict:
        """Decodes a JWT token and returns the payload as a dictionary.
        Args:
        token: The JWT token string.
        Returns:
        A dictionary containing the decoded payload or None if decoding fails.
        """
        try:
            token = self.get_token(request=request)
            jwt_signing_key = env("JWT_SIGNING_KEY")
            payload = jwt.decode(jwt=token, key=jwt_signing_key, algorithms=["HS256"])
            return payload  # payload has additional user details. see Auth Service's CustomTokenObtainPairSerializer
        except jwt.DecodeError:
            logger.error("\n[X]: JWT signature verification failed")
            return None


class ProcessData(DecodeJWT):
    """Process Data Util Class. Returns Payload from JWT and Testcases from Questions Model."""

    def generate_submission_uuid(self) -> uuid.UUID:
        """Generates a unique UUID combining current time, process id and a uuid int.
        Args:
            None
        Return:
            A UUID4 object.
        """
        # current time in milliseconds
        timestamp = int(time.time() * 1000)
        # process ID
        process_id = getpid()
        # take int of an uuid
        random_number = uuid.uuid4().int
        # generate an unique UUID
        custom_uuid = uuid.UUID(int=(timestamp + process_id + random_number))
        return custom_uuid

    # main entrypoint of processing data.
    def process_data(self, request, problem_id) -> dict:
        """Utility function to gather all the required data to upload to s3
        Args:
            HTTP Request object, Questions model id
        Return:
            A dict with user details from jwt claim, submission_uuid_id and testcases from Questions model.
        """
        # get the payload from jwt
        payload = self.decode_jwt(request=request)
        if payload is not None:
            user_details = {
                "user_id": payload.get("user_id"),
                "username": payload.get("username"),
                "email": payload.get("email"),
            }
            # generate a UUID for submission id
            submission_id = self.generate_submission_uuid()
            try:
                problem_test_cases = Questions.objects.get(id=problem_id).test_cases
            except (ValidationError, Questions.DoesNotExist):
                logger.error(f"\n[X]: No question available with the ID: {problem_id}")
                return None, "problem_id_error"
            data = {
                "user": user_details,
                "submission_id": str(
                    submission_id
                ),  # submission_id is an object of UUID, convert obj it to str
                "test_cases": problem_test_cases,
            }
            return data, "success"
        else:
            return None, "jwt_decode_error"


class UploadToS3:
    """Upload user code and other data to s3 bucket."""

    def __get_client(self):
        return boto3.client("s3")

    def upload_file_to_s3(self, object_key, bytes_obj_data):
        """Upload file to the s3 bucket."""

        s3_client = self.__get_client()
        bucket_name = env("AWS_STORAGE_BUCKET_NAME")
        try:
            # use any of the follwoing method. both works well with bytes data.
            # s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=bytes_obj_data)

            s3_client.upload_fileobj(bytes_obj_data, bucket_name, object_key)
            file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_key}"
            return file_url, "success"

        except S3UploadFailedError as e:
            logger.error(f"\n[X]: Error #Uploading User Code Files to S3: {e}")
            return None, "error-data-handling-to-s3"
        except S3TransferFailedError as e:
            logger.error(f"\n[X]: Error #Transferring User Codes Files to S3: {e}")
            return None, "error-data-handling-to-s3"
        except Exception as e:
            logger.error(f"\n[X]: Error #Handling User Codes Files to S3: {e}")
            return None, "error-data-handling-to-s3"


"""some alternate util codes"""


class UploadToS3_2:
    """Upload User Codes to S3 Bucket. Uses Sesstion to create s3 client."""

    # also works. but need to use env files here to create session. The below UploadToS3 is alternate approach.
    @classmethod
    def __get_client(cls):
        # using sesstion
        session = boto3.Session(
            aws_access_key_id=env("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env("AWS_SECRET_ACCESS_KEY"),
        )
        s3_client = session.client("s3")
        return s3_client

    @staticmethod
    def upload_file(object_key, bytes_obj_data):  # objec_key = file name
        """Upload file to the s3 bucket."""
        s3_client = UploadToS3.__get_client()
        bucket_name = env("AWS_STORAGE_BUCKET_NAME")

        # use any of the follwoing method. both works well with bytes data.
        # s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_obj_data)

        s3_client.upload_fileobj(bytes_obj_data, bucket_name, object_key)

        # file url
        file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_key}"
        return file_url


def generate_submission_id_hex() -> str:
    """Generates a unique Hex ID
    Args:
        None
    Return:
        A SHA256 hex string.
    """
    # current timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    process_id = getpid()
    uuid_int_key = uuid.uuid4().int
    data = str(timestamp) + str(process_id) + str(uuid_int_key)
    # hash the unique str
    unique_id = hashlib.sha256(data.encode()).hexdigest()
    # although the unique_id is not convertable to any uuid version, but it is much unique and hashed.
    return unique_id


# if __name__ == "__main__":
jwt_decoder = DecodeJWT()
s3_data_processor = ProcessData()
s3_data_uploader = UploadToS3()
