from flask import Flask
import pika
import uuid
import json
import threading

server = Flask(__name__)

class RpcClient(object):

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

    def call(self, req):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        #добавить в дальнейшем в пропертис - application/json в content-type свойство
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            #Изменить body
            body=str(req))
        while self.response is None:
            self.connection.process_data_events()
        print(self.response)
        return self.response

rpc_get = RpcClient()

@server.route('/myproject/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    my_thread = threading.Thread(target=rpc_get.call, args=(int(task_id),))
    my_thread.start()
    my_thread.join()
    return "sent " + str(task_id) + "\n" + str(rpc_get.response) + "\n"

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0')
