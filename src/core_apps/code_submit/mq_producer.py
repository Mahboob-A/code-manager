# python
import os, json, logging

# django
from django.conf import settings

# pika
import pika

logger = logging.getLogger(__name__)


class CloudAMQPHealper:
    """CloudAMQP Helper Class to Declare Exchange and Queue"""

    def __init__(self) -> None:
        self.broker_url = settings.CLOUD_AMQP_URL
        self.params = pika.URLParameters(self.broker_url)

    def connect(self):
        self.__connection = pika.BlockingConnection(parameters=self.params)
        self.channel = self.__connection.channel()

    def prepare_exchange_and_queue(self) -> None:
        # exchange declare
        self.channel.exchange_declare(
            exchange=settings.EXCHANGE_NAME, exchange_type=settings.EXCHANGE_TYPE
        )
        # declare queue
        self.channel.queue_declare(queue=settings.QUEUE_NAME)
        # binding exchange and queue
        self.channel.queue_bind(
            settings.QUEUE_NAME, settings.EXCHANGE_NAME, settings.BINDING_KEY
        )


class DataPublisherMQ(CloudAMQPHealper):
    """Interface class to publish data to MQ"""

    def publish_data(self, uploaded_s3_data_link: str, object_key: str) -> None:
        # connect to mq and prepare exchange and queue

        try:
            self.connect()
            self.prepare_exchange_and_queue()
            self.channel.basic_publish(
                exchange=settings.EXCHANGE_NAME,
                routing_key=settings.ROUTING_KEY,
                body=uploaded_s3_data_link,
            )
            logger.info(
                f"\n[MQ SUCCESS]: The User Code Files with Object Key: '{object_key}' Successfully Published to MQ."
            )
            return True, "success"
        except Exception as e:
            logger.exception(
                f"\n[MQ ERROR]: The User Code Files with Object Key: '{object_key}' Could not be published to MQ.\n[MQ EXCEPTION]: {str(e)}"
            )
            return None, "error-publishing-to-mq"


# instance to call
mq_publisher = DataPublisherMQ()
