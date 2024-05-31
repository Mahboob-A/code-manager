# python
import json
import logging
import time


# django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status

# drf
from rest_framework.response import Response
from rest_framework.views import APIView

# mongodb
from db_connection import mongo_result_collection

# others
import redis

logger = logging.getLogger(__name__)


try:
    redis_client = redis.Redis(host="code-manager-redis", port=6379, db=0)
except (ImproperlyConfigured, Exception) as e:
    logger.exception(
        f"\n[Redis Import Error]: Error Occurred During Importing Reids\n[EXCEPTION]: {str(e)}"
    )
    raise ImproperlyConfigured("Redis is not available")


class CodeExecutionResultAPI(APIView):
    """API for Result of the Code Execution using Polling Technique."""

    def success_response(self, data):
        """Return a success response."""
        return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)

    def check_database_and_update_cache(self, submission_id):
        """Check the result in the database and update the cache if found."""
        db_result: dict = mongo_result_collection.find_one(
            {"submission_id": submission_id}
        )
        if db_result:
            # Delete the MongoDB specific ID.
            db_result.pop("_id")
            # Set the cache
            redis_client.set(
                name=submission_id, value=json.dumps(db_result)
            )  # save the data as json (dict to json)
            redis_client.expire(
                name=submission_id, time=settings.REDIS_CACHE_TIME_IN_SECONDS
            ) # currently 15 seconds 
            return db_result
        return None

    def get(self, request, submission_id):
        """Returns the Code Execution Result for the given submission_id."""
        timeout = 5
        retry_interval = 0.5
        start_time = time.time()

        cache_result: bytes = redis_client.get(submission_id)
        if cache_result is not None:
            logger.info(f"\n\n[Cache HIT]: Cache Hit for Submission ID: {submission_id}")
            # making the bytes data to dict for better serialization.
            # without making it dict, would also work. bytes to dict
            return self.success_response(json.loads(cache_result))

        db_result: dict = self.check_database_and_update_cache(submission_id)
        if db_result is not None:
            logger.info(f"\n\n[DB HIT]: DB Hit for Submission ID: {submission_id}")
            return self.success_response(db_result)

        polling_data_success = False 
        # long polling start as the data could not be founf in teh cache as well as in the db
        logger.info(f"\n\n[Polling STARTED]: Polling Started for Submittion ID: {submission_id}")
        while time.time() - start_time < timeout:
            cache_result: json = redis_client.get(submission_id)
            print('submission id in while loop: ', submission_id)
            if cache_result:
                logger.info(
                    f"\n\n[Polling HIT]: Polling Hit for Submittion ID: {submission_id}"
                )
                polling_data_success = True 
                return self.success_response(json.loads(cache_result))
            time.sleep(retry_interval)

        if polling_data_success is False: 
            logger.info(
                f"\n\n[Polling DATA MISS]: Polling  Data Miss for Submittion ID: {submission_id}\nData is still not Available for Submission ID: {submission_id}"
            )
            return Response(
                {"status": "pending", "data": None}, status=status.HTTP_202_ACCEPTED
            )
