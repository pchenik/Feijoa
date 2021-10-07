# Feijoa
"RabbitMQ/Flask/Worker/Archive" service

# Docker Compose
*All services are distributed among four docker containers. To make them work we need use the following command to start all processes:*
```
**$ docker compose-up -d**
Creating whole_project_rabbitmq_1 ... done
Creating whole_project_server_1   ... done
Creating whole_project_worker_1   ... done
Creating whole_project_archive_1  ... done
```

# Send request
*To get a task (id 1-3 for now) from dictionary we'll use the HTTP's GET method:*

**curl -i http://localhost:5000/myproject/v1.0/tasks/3**

HTTP/1.0 200 OK
**Content-Type**: text/html; charset=utf-8
**Content-Length**: 120
**Server**: Werkzeug/2.0.1 Python/3.6.9
**Date**: Thu, 07 Oct 2021 00:02:11 GMT

sent 3
b'{"task": {"id": 3, "title": "Compete on Codeforces", "description": "Get to the first place", "done": false}}'

*There'll be more request types in the near future*
