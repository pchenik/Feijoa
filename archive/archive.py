import json
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='arch_queue')

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
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
    get_req = json.loads(body)

    response = {'status': 404, 'response': {}}

    if get_req['methods'] == 'GET':
        if get_req['id'] == None:
            response = {'status': 'OK', 'response': tasks}
        else:
            task_id = get_req['id']
            print(" [.] task_id(%s)" % task_id)
            task = list(filter(lambda t: t['id'] == task_id, tasks))
            response = {'status' : 'OK' if task else '404', 'response': task[0]}
    elif get_req['methods'] == 'POST':
        task = get_req['task']
        task['id'] = len(tasks) + 1
        tasks.append(task)
        response = {'status': 'OK', 'response': 'Task {} has been successfully added'.format(task['id'])}
        #print(response)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='arch_queue', on_message_callback=on_request2)

print(" [x] Awaiting RPC requests from worker's queues")
channel.start_consuming()
