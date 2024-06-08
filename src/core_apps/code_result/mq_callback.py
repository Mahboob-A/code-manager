import json
import logging
import time
import traceback


import redis
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

# mongodb
from db_connection import mongo_result_collection

# # MQ Code Execution Result Consume
from core_apps.code_result.code_exec_result_consumer import result_consumer_mq

logger = logging.getLogger(__name__)


try:
    redis_client = redis.Redis(host="code-manager-redis", port=6379, db=0)
except (ImproperlyConfigured, Exception) as e:
    logger.exception(
        f"\n[Redis Import Error]: Error Occurred During Importing Reids\n[EXCEPTION]: {str(e)}"
    )
    raise ImproperlyConfigured("Redis is not available")


def callback(channel, method, properties, body):
    """The callback function consumes from the Code Result Execution Queue
    Published by RCE Engine.

    The Callback does the following:
    A. The callback consumes code execution result from Code Result Execution Queue
         Published by RCE Engine.

     B. It then Saves the result in DB.
    """
    try:
        # body is in bytes. decodes to str then as dict
        result_data = json.loads(body.decode("utf-8"))


        # cached for immediate polling
        submission_id = result_data.get("submission_id")
        redis_client.set(submission_id, json.dumps(result_data))  #save as json 
        redis_client.expire(
            name=submission_id, time=settings.REDIS_CACHE_TIME_IN_SECONDS
        )  # currently 15 seconds

        # saved in mongodb 
        mongo_result_collection.insert_one(result_data)

        username = result_data["user_details"].get("username")
        logger.info(
            f"\n\n[Code Result Consume Success]: Code Result Consume Successful for Username: {username}"
        )
    except Exception as e:
        logger.exception(
            f"\n\n[MQ Callback EXCEPTION]: Exception Occurred at Callback while Consuming Code EXEC Results\n[EXCEPTION]: {str(e)}"
        )
        logger.error("\nTraceback")
        traceback.print_exc()


def main():
    logger.info(f"\n\n[In MAIN]: In main Func of Callback.")
    result_consumer_mq.consume_messages(callback=callback)
