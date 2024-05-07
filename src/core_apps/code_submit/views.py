# python
import logging
import io
import json
import time

# django
from django.shortcuts import render
from django.conf import settings

# drf
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# others
import boto3

# local
from core_apps.code_submit.utils import jwt_decoder, s3_data_processor, s3_data_uploader

logger = logging.getLogger(__name__)


class TestAPI(APIView):
    """Test API to test the JWT token payload."""

    def get(self, request, format=None):
        payload = jwt_decoder.decode_jwt(request=request)
        logging.info(f"\npayload is: {payload}")  # dict
        return Response({"ok"})


class SubmitCode(APIView):
    """Submit Code to the code-manager service"""

    def process_error_response(self, message, problem_id=None) -> Response:
        if message == "jwt_decode_error":
            return Response(
                {"detail": "The JWT Token could not be verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if message == "problem_id_error":
            return Response(
                {"detail": f"The problem id {problem_id} is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if message == "error-data-handling-to-s3":
            return Response(
                {
                    "detail": "Something went wrong at our end. Please try again after sometime."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, format=None):
        problem_id = request.data.get("problem_id")
        lang = request.data.get("lang")

        # process the data that needs to be uploaded in the s3 bucket.
        data, message = s3_data_processor.process_data(
            request=request, problem_id=problem_id
        )
        if data is not None:
            now = int(time.time())
            username = data["user"].get("username")

            # convert data to string to convert it into bytes
            data = json.dumps(data)
            bytes_obj_data = io.BytesIO(data.encode())

            file_prefix = f"{username}-{now}-{lang}"
            object_key = f"codes/{file_prefix}-data.txt"  # object_key is the filename

            # Upload to S3
            file_url, message = s3_data_uploader.upload_file_to_s3(
                object_key=object_key, bytes_obj_data=bytes_obj_data
            )

            # file_url == s3 upload success 
            if file_url is not None:
                logger.info(
                    f"\n[S]: The User Code Files with Object Key: '{object_key}' Successfully Uploaded to S3."
                )
                pass
            else:
                logger.error(
                    f"\n[X]: The Object Key: {object_key} could not be Uploaded to S3."
                )
                return self.process_error_response(message=message)
            # upload_file() # uploading file is done.
            # s3_link = upload_to_s3() # done
            # pushed_to_rabbit_mq()
            # return success response
        else:
            logger.error(f"\n[X]: Data could not be processed. The error is: {message}")
            return self.process_error_response(message=message, problem_id=problem_id)

        return Response({"ok"})
