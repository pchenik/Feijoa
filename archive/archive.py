import json
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))

channel = connection.channel()

channel.queue_declare(queue='arch_queue')

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn RabbitMQ',
        'description': u'Need to find a good tutorial on the web',
        'done': False
    },
    {
        'id': 3,
        'title': u'Compete on Codeforces',
        'description': u'Get to the first place',
        'done': False
    }
]


def on_request2(ch, method, props, body):
    task_id = int(body)
    print(" [.] task_id(%s)" % task_id)

    task = list(filter(lambda t: t['id'] == task_id, tasks))
    # if len(task) == 0:
    #     response =
    # else
    response = {'task': task[0]}

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='arch_queue', on_message_callback=on_request2)

print(" [x] Awaiting RPC requests from worker's queues")
channel.start_consuming()
