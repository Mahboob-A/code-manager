# python
import logging

# django
from django.conf import settings

# other
import boto3
from boto3.exceptions import S3TransferFailedError, S3UploadFailedError
from botocore.exceptions import ClientError, UnknownEndpointError, UnknownKeyError


logger = logging.getLogger(__name__)


class S3DataHandler:
    """Upload user code and other data to s3 bucket."""

    def __get_client(self):
        return boto3.client("s3")

    def upload_file_to_s3(self, object_key, bytes_obj_data):
        """Upload file to the s3 bucket."""

        try:
            s3_client = self.__get_client()
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            # use any of the follwoing method. both works well with bytes data.
            # s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=bytes_obj_data)

            s3_client.upload_fileobj(bytes_obj_data, bucket_name, object_key)
            file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_key}"
            logger.info(
                f"\n[S3 SUCCESS]: The User Code Files with Object Key: '{object_key}' Successfully Uploaded to S3."
            )
            return file_url, "success"

        except S3UploadFailedError as e:
            logger.error(
                f"\n[S3: ERROR]: Error #Uploading Object Key - '{object_key}' to S3: {e}"
            )
            return None, "error-data-handling-to-s3"
        except S3TransferFailedError as e:
            logger.error(
                f"\n[S3 ERROR]: Error #Transferring Object Key - '{object_key}' to S3: {e}"
            )
            return None, "error-data-handling-to-s3"
        except Exception as e:
            logger.exception(
                f"\n[S3 ERROR]: Error #Handling Object Key - '{object_key}' to S3: {e}"
            )
            return None, "error-data-handling-to-s3"

    def delete_uploaded_file(self, object_key: str) -> None:
        """delete the uploaded file if the link could not be pushed to mq"""
        try:
            s3_client = self.__get_client()
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            logger.info(
                f"\n[S3 SUCCESS] The Object Key {object_key} has been DELETED."
            )
        except (ClientError, UnknownEndpointError, UnknownKeyError, Exception) as e:
            logger.exception(
                f"\n[S3 ERROR]: Error Occurred During File Deletion from S3\n[S3 EXCEPTION]: {str(e)}"
            )


"""POC: alternate class using boto3 Session"""


class UploadToS3_2:
    """Upload User Codes to S3 Bucket. Uses Sesstion to create s3 client."""

    # also works. but need to use env files here to create session. The upper UploadToS3 is an alternate approach.
    @classmethod
    def __get_client(cls):
        # using sesstion
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3_client = session.client("s3")
        return s3_client

    @staticmethod
    def upload_file(object_key, bytes_obj_data):  # objec_key = file name
        """Upload file to the s3 bucket."""
        s3_client = UploadToS3_2.__get_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        # use any of the follwoing method. both works well with bytes data.
        # s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_obj_data)

        s3_client.upload_fileobj(bytes_obj_data, bucket_name, object_key)

        # file url
        file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_key}"
        return file_url


# instance to call
s3_data_handler = S3DataHandler()
