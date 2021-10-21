from flask import Flask, jsonify, abort, make_response, request, url_for
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
            self.response = json.loads(body)

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
            body=req)
        while self.response is None:
            self.connection.process_data_events()
        #Обработка ответа
        #ans = json.loads(self.response)
        print(self.response)
        return self.response

rpc_get = RpcClient()

@server.route('/myproject/v1.0/tasks', methods=['GET'])
def get_tasks():
    req = {'methods': 'GET', 'id': None}
    my_thread = threading.Thread(target=rpc_get.call, args=(json.dumps(req),))
    my_thread.start()
    my_thread.join()
    return "sent ALL" + "\n" + str(rpc_get.response) + "\n"

@server.route('/myproject/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    req = {'methods': 'GET', 'id': task_id}
    my_thread = threading.Thread(target=rpc_get.call, args=(json.dumps(req),))
    my_thread.start()
    my_thread.join()
    return "sent " + str(task_id) + "\n" + str(rpc_get.response) + "\n"

@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@server.route('/myproject/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    req = {'methods': 'POST', 'task': {'id': request.json.get('id', 0), 'title': request.json['title'],
                                       'description': request.json.get('description', ""), 'done': False}}
    my_thread = threading.Thread(target=rpc_get.call, args=(json.dumps(req),))
    my_thread.start()
    my_thread.join()
    #tasks.append(task)
    return "sent POST" + "\n" + str(rpc_get.response) + "\n"


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0')
