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
from core_apps.common.jwt_decode import jwt_decoder
from core_apps.code_submit.process_data import data_processor
from core_apps.code_submit.code_submission_producer import code_submission_publisher_mq


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

    def post(self, request, format=None):
        """Decode JWT, get user details. Get Testcases from DB. Upload data to S3. Push FIle Link to MQ"""
        problem_id = request.data.get("problem_id")
        lang = request.data.get("lang")
        code = request.data.get("code")

        # process the data that needs to be publish to the MQ.
        data, message = data_processor.process_data(
            request=request, problem_id=problem_id, lang=lang, code=code
        )
        if data is not None:
            submission_id = data.get("submission_id")

            username = data["user_details"].get("username")
            data = json.dumps(data)

            # publish to MQ
            published, message = code_submission_publisher_mq.publish_data(
                user_code_data=data, username=username
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
                return self.process_error_response(message=message)
        else:
            # jwt or fetch question details in data process failed.
            return self.process_error_response(message=message, problem_id=problem_id)
