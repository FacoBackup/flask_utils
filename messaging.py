import pika, json
from pika import exceptions
from sqlalchemy.exc import SQLAlchemyError
from app import db


class Messaging:
    def __init__(self, host, user, user_password, port=5672):
        self.host = host
        self.port = port
        self.user = user
        self.user_password = user_password

    def consumer(self, callback, queue):
        try:
            credentials = pika.PlainCredentials(self.user, self.user_password)
            params = pika.ConnectionParameters(self.host, self.port, '/', credentials)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue=queue)

            channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
            channel.close()
        except (exceptions.ProbableAccessDeniedError, exceptions.ChannelClosedByBroker):
            pass

    def publish(self, method, body, routing):
        try:
            credentials = pika.PlainCredentials(self.user, self.user_password)
            params = pika.ConnectionParameters(self.host, self.port, '/', credentials)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            properties = pika.BasicProperties(method)
            channel.basic_publish(exchange='', routing_key=routing, body=json.dumps(body), properties=properties)
        except (
                exceptions.ProbableAccessDeniedError,
                exceptions.ChannelClosedByBroker,
                exceptions.StreamLostError,
                exceptions.AMQPConnectionError
        ):
            pass
