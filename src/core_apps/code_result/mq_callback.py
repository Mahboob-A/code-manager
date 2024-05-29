import json
import logging
import time
import traceback

import redis
from django.core.exceptions import ImproperlyConfigured

# # MQ Code Execution Result Consume
from core_apps.code_result.code_exec_result_consumer import result_consumer_mq

logger = logging.getLogger(__name__)


try:
    r = redis.Redis(host="code-manager-redis", port=6379, db=0)
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
        print("\n\nResult Data In Code Manager: ", result_data)

        # Save the result in cache  for immediate polling
        submission_id = result_data.get("submission_id")
        r.set(submission_id, json.dumps(result_data))
        r.expire(name=submission_id, time=60)

        # save the result in db for persistence.

        username = result_data["user_details"].get("username")

        logger.info(
            f"[Code Result Consume Success]: Code Result Consume Successful for Username: {username}"
        )

    except Exception as e:
        logger.exception(
            f"[MQ Callback EXCEPTION]: Exception Occurred at Callback.\n[EXCEPTION]: {str(e)}"
        )
        logger.error("\nTraceback")
        traceback.print_exc()


def main():
    logger.info(f"\n[In MAIN]: In main Func of Callback.")
    result_consumer_mq.consume_messages(callback=callback)
