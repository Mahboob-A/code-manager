# python
import os, json, logging
from typing import Callable

# django
from django.conf import settings

# pika
import pika

logger = logging.getLogger(__name__)


class CloudAMQPHandler:
    """CloudAMQP Handler Class to Declare Exchange and Queue
    for Code Result Consumption [Published by RCE Engine Service]
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
            exchange=settings.RESULT_PUBLISH_EXCHANGE_NAME,
            exchange_type=settings.RESULT_PUBLISH_EXCHANGE_TYPE,
        )
        # declare queue
        self.channel.queue_declare(queue=settings.RESULT_PUBLISH_QUEUE_NAME)
        # binding exchange and queue
        self.channel.queue_bind(
            settings.RESULT_PUBLISH_QUEUE_NAME,
            settings.RESULT_PUBLISH_EXCHANGE_NAME,
            settings.RESULT_PUBLISH_BINDING_KEY,
        )


class CodeEXECResultConsumerMQ(CloudAMQPHandler):
    """Interface class to publish data to MQ
        Consume Code Execution Result from Result Queue [Published by RCE Engine Service]
    """
    def consume_messages(self, callback: Callable) -> None:
        try:
            self.connect()
            self.prepare_exchange_and_queue()

            self.channel.basic_consume(
                settings.RESULT_PUBLISH_QUEUE_NAME, callback, auto_ack=True
            )

            logger.info(
                f"\n[MQ Consume BEGIN]: Message Consumption from Result Publish Queue Started."
            )
            self.channel.start_consuming()
            logger.info(
                f"\n[MQ Consume SUCCESS]: Message Consuming Finished from Result Publish Queue."
            )
        except Exception as e:
            logger.exception(
                f"\n[MQ Consumer EXCEPTION]: Exception Occurred During Cnsuming Messages from Result Publish MQ\n[EXCEPTION]: {str(e)}\n"
            )


# instance to call
result_consumer_mq = CodeEXECResultConsumerMQ()
