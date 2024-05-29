# python
import json
import logging
import time

# others
import redis

# django
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status

# drf
from rest_framework.response import Response
from rest_framework.views import APIView

# local
from core_apps.common.jwt_decode import jwt_decoder

logger = logging.getLogger(__name__)


try:
    redis_client = redis.Redis(host="code-manager-redis", port=6379, db=0)
except (ImproperlyConfigured, Exception) as e:
    logger.exception(
        f"\n[Redis Import Error]: Error Occurred During Importing Reids\n[EXCEPTION]: {str(e)}"
    )
    raise ImproperlyConfigured("Redis is not available")


class CodeExecutionResultAPI(APIView):
    """API for Result of the Code Execution.
    The API uses Polling Technique.

    Args:
        Str: submission_id

    Return:
        JSON: Code Execution Result
    """

    def get(self, request, submission_id):
        """Returns the Code Execution Result Provided the submission_id"""
        timeout: int = 15
        retry_interval: float = 0.1
        start_time: time = time.time()

        # implement get data from db, in case data not found in cache.
        while time.time() - start_time < timeout:
            result: json = redis_client.get(submission_id)
            if result:
                result_data: dict = json.loads(result)
                return Response(
                    {"status": "success", "data": result_data},
                    status=status.HTTP_200_OK,
                )
            time.sleep(retry_interval)

        return Response(
            {"status": "pending", "data": None}, status=status.HTTP_202_ACCEPTED
        )
