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

    def prepare_exchange_and_queue(self, lang: str) -> None:

        # NOTE exchange declare based on lang type. to mitigate fault tolerant, isolation, and potential scalability, 
        # two separate exchanges have been used. If singe exchage is used, and somehow it failes, 
        # all the routing for all the queue will be stopped.  Hence, for potential fault tolerant, using two separate exchanges. 
        # NOTE lang is universally in lowecase from the API call. 
        if lang == 'cpp': 
            self.channel.exchange_declare(
                exchange=settings.CPP_CODE_SUBMISSION_EXCHANGE_NAME,
                exchange_type=settings.CPP_CODE_SUBMISSION_EXCHANGE_TYPE,
            )
            self.channel.queue_declare(queue=settings.CPP_CODE_SUBMISSION_QUEUE_NAME)
        
            self.channel.queue_bind(
                settings.CPP_CODE_SUBMISSION_QUEUE_NAME,
                settings.CPP_CODE_SUBMISSION_EXCHANGE_NAME,
                settings.CPP_CODE_SUBMISSION_BINDING_KEY,
            )
        else: # NOTE lang is java, create connection for java exchange and queue. 
            self.channel.exchange_declare(
                exchange=settings.JAVA_CODE_SUBMISSION_EXCHANGE_NAME,
                exchange_type=settings.JAVA_CODE_SUBMISSION_EXCHANGE_TYPE,
            )
            self.channel.queue_declare(queue=settings.JAVA_CODE_SUBMISSION_QUEUE_NAME)
            self.channel.queue_bind(
                settings.JAVA_CODE_SUBMISSION_QUEUE_NAME,
                settings.JAVA_CODE_SUBMISSION_EXCHANGE_NAME,
                settings.JAVA_CODE_SUBMISSION_BINDING_KEY,
            )

class CodeSubmissionPublisherMQ(CloudAMQPHandler):
    """Interface Class to Publish Message to Publish Code Submission Queue"""

    def publish_data(self, user_code_data: json, username: str, lang: str) -> None:
        # connect to mq and prepare exchange and queue

        try:
            self.connect()

            # prepare connection and channel based on the lang
            self.prepare_exchange_and_queue(lang=lang)

            # publish the message based on the lang to appropriate queue
            # NOTE lang is universally in lowecase from the API call.
            if lang == 'cpp': 
                self.channel.basic_publish(
                    exchange=settings.CPP_CODE_SUBMISSION_EXCHANGE_NAME,
                    routing_key=settings.CPP_CODE_SUBMISSION_ROUTING_KEY,
                    body=user_code_data,
                )
            else:  # NOTE lang is java. publish to java queue. 
                self.channel.basic_publish(
                    exchange=settings.JAVA_CODE_SUBMISSION_EXCHANGE_NAME,
                    routing_key=settings.JAVA_CODE_SUBMISSION_ROUTING_KEY,
                    body=user_code_data,
                )

            logger.info(
                f"\n[MQ SUCCESS]: The User Code Files of UseName: '{username}' of Language: '{lang}' Successfully Published to Submission MQ."
            )
            message = "success"
            return True, message
        except Exception as e:
            logger.exception(
                f"\n[MQ ERROR]: The User Code Files of UN: '{username}' of Language: '{lang}' Could not be published to Submission MQ.\n[MQ EXCEPTION]: {str(e)}"
            )
            message = "error-publishing-to-code-submission-mq"
            return False, message


# instance to call
code_submission_publisher_mq = CodeSubmissionPublisherMQ()
