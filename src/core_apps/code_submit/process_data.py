# python
import jwt
import logging
import uuid
import time
from os import getpid

# django
from django.core.exceptions import ValidationError

# local
from core_apps.code_display.models import Questions
from core_apps.code_submit.jwt_decode import DecodeJWT

logger = logging.getLogger(__name__)


class ProcessData(DecodeJWT):
    """Process Data Util Class. Returns Payload from JWT and Testcases from Questions Model."""

    def generate_submission_uuid(self) -> uuid.UUID:
        """Generates a unique UUID combining current time, process id and a uuid int.
        Args:
            None
        Return:
            A UUID4 object.
        """
        # time in milliseconds
        timestamp = int(time.time() * 1000)
        process_id = getpid()
        random_number = uuid.uuid4().int
        custom_uuid = uuid.UUID(int=(timestamp + process_id + random_number))
        return custom_uuid

    # main entrypoint of processing data.
    def process_data(self, request, problem_id: str, lang: str) -> dict:
        """Utility function to gather all the required data to upload to s3
        Args:
            HTTP Request object, Questions model id
        Return:
            A dict with user details from jwt claim, submission_uuid_id and testcases from Questions model.
        """
        # the payload from jwt
        payload = self.decode_jwt(request=request)
        if payload is not None:
            user_details = {
                "user_id": payload.get("user_id"),
                "username": payload.get("username"),
                "email": payload.get("email"),
            }
            # an UUID for submission id
            submission_id = self.generate_submission_uuid()
            try:
                testcases_inputs, testcases_answers = Questions.objects.values_list(
                    "testcases_inputs", "testcases_answers"
                ).get(id=problem_id)
            except (ValidationError, Questions.DoesNotExist):
                message = "problem-id-error"
                logger.error(
                    f"\n[DATA PROCESS ERROR]: No question available with the ID: {problem_id}"
                )
                return None, message
            data = {
                "user_details": user_details,
                "submission_id": str(
                    submission_id
                ),  # submission_id is an object of UUID, convert obj it to str
                "lang": lang,
                "testcase_inputs": testcases_inputs,
                "testcase_answers": testcases_answers,
            }
            message = "success"
            return data, message
        else:
            message = "jwt-decode-error"
            logger.error(
                f"\n[DATA PROCESS ERROR]: Data could not be processed. The error is: {message}"
            )
            return None, message


# instance to call
data_processor = ProcessData()
