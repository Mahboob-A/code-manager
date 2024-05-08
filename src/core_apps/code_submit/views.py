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
from core_apps.code_submit.jwt_decode import jwt_decoder
from core_apps.code_submit.process_data import data_processor
from core_apps.code_submit.s3_handler import s3_data_handler
from core_apps.code_submit.mq_producer import mq_publisher


logger = logging.getLogger(__name__)


class TestAPI(APIView):
    """Test API to test the JWT token payload."""

    def get(self, request, format=None):
        payload = jwt_decoder.decode_jwt(request=request)
        logging.info(f"\npayload is: {payload}")  # dict
        return Response({"ok"})


class SubmitCode(APIView):
    """Submit Code to the code-manager service"""

    def process_error_response(self, message: str, problem_id: str = None) -> Response:
        if message == "jwt-decode-error":
            return Response(
                {"detail": "The JWT Token could not be verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if message == "problem-id-error":
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
        if message == "error-publishing-to-mq":
            return Response(
                {
                    "detail": "Something went wrong at our end. Please try again after sometime."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create_unique_object_key(self, data, lang):
        """Create an Unique filename for S3 Upload"""
        now = int(time.time())
        username = data["user"].get("username")
        file_prefix = f"{username}-{now}-{lang}"
        object_key = f"codes/{file_prefix}-data.txt"
        return object_key

    def s3_upload(self, data, object_key):
        """Upload to S3"""
        data = json.dumps(data)
        bytes_obj_data = io.BytesIO(data.encode())
        # Upload to S3
        s3_file_url, message = s3_data_handler.upload_file_to_s3(
            object_key=object_key, bytes_obj_data=bytes_obj_data
        )
        return s3_file_url, message

    def post(self, request, format=None):
        """Decode JWT, get user details. Get Testcases from DB. Upload data to S3. Push FIle Link to MQ"""
        problem_id = request.data.get("problem_id")
        lang = request.data.get("lang")

        # process the data that needs to be uploaded in the s3 bucket.
        data, message = data_processor.process_data(
            request=request, problem_id=problem_id
        )
        if data is not None:
            submission_id = data.get("submission_id")

            object_key = self.create_unique_object_key(data=data, lang=lang)
            s3_file_url, message = self.s3_upload(data=data, object_key=object_key)

            # s3_file_url == s3 upload success. publish to mq
            if s3_file_url is not None:
                published, message = mq_publisher.publish_data(
                    uploaded_s3_data_link=s3_file_url, object_key=object_key
                )
                if published:
                    return Response(
                        {
                            "result": {
                                "detail": "Your response has been submitted.",
                                "submission_id": submission_id,
                            }
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    # s3 data link publish to MQ failed. delete s3 data link from s3 bucket
                    s3_data_handler.delete_uploaded_file(object_key)
                    return self.process_error_response(message=message)
            else: 
                # data upload to s3 failed.
                return self.process_error_response(message=message)
        else: 
            # jwt and fetch question details in data process failed.
            return self.process_error_response(message=message, problem_id=problem_id)
