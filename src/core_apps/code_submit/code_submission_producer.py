# python
import json
import logging
import os

# pika
import pika

# django
from django.conf import settings

logger = logging.getLogger(__name__)


class CloudAMQPHandler:
    """CloudAMQP Helper Class to Declare Exchange and Queue
    for Code Submission Publication
    """

    def __init__(self) -> None:
        self.broker_url = settings.CLOUD_AMQP_URL
        self.params = pika.URLParameters(self.broker_url)

    def connect(self):
        self.__connection = pika.BlockingConnection(parameters=self.params)
        self.channel = self.__connection.channel()

    def prepare_exchange_and_queue(self) -> None:
        # exchange declare
        self.channel.exchange_declare(
            exchange=settings.CODE_SUBMISSION_EXCHANGE_NAME,
            exchange_type=settings.CODE_SUBMISSION_EXCHANGE_TYPE,
        )
        # declare queue
        self.channel.queue_declare(queue=settings.CODE_SUBMISSION_QUEUE_NAME)
        # binding exchange and queue
        self.channel.queue_bind(
            settings.CODE_SUBMISSION_QUEUE_NAME,
            settings.CODE_SUBMISSION_EXCHANGE_NAME,
            settings.CODE_SUBMISSION_BINDING_KEY,
        )


class CodeSubmissionPublisherMQ(CloudAMQPHandler):
    """Interface Class to Publish Message to Publish Code Submission Queue"""

    def publish_data(self, user_code_data: json, username: str) -> None:
        # connect to mq and prepare exchange and queue

        try:
            self.connect()
            self.prepare_exchange_and_queue()
            self.channel.basic_publish(
                exchange=settings.CODE_SUBMISSION_EXCHANGE_NAME,
                routing_key=settings.CODE_SUBMISSION_ROUTING_KEY,
                body=user_code_data,
            )
            logger.info(
                f"\n[MQ SUCCESS]: The User Code Files of UN: '{username}' Successfully Published to Submission MQ."
            )
            message = "success"
            return True, message
        except Exception as e:
            logger.exception(
                f"\n[MQ ERROR]: The User Code Files of UN: '{username}' Could not be published to Submission MQ.\n[MQ EXCEPTION]: {str(e)}"
            )
            message = "error-publishing-to-code-submission-mq"
            return False, message


# instance to call
code_submission_publisher_mq = CodeSubmissionPublisherMQ()
