import json
import pika
import uuid


class WorkerRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))

channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

rpc_worker = WorkerRpcClient()


def on_request(ch, method, props, body):
    rpc_worker.response = None
    rpc_worker.corr_id = props.correlation_id
    # добавить в дальнейшем в пропертис - application/json в content-type свойство
    rpc_worker.channel.basic_publish(
        exchange='',
        routing_key='arch_queue',
        properties=pika.BasicProperties(
            reply_to=rpc_worker.callback_queue,
            correlation_id=props.correlation_id,
        ),
        # Изменить body
        body=body)

    while rpc_worker.response is None:
        rpc_worker.connection.process_data_events()

    # по возвращению из archive - сделать какой-то вывод или действие над объектом???
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=rpc_worker.response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print(" [x] Successfully transmitted to the archive and back to the server")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests from rpc_queue")
channel.start_consuming()
