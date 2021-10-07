# Feijoa
"RabbitMQ/Flask/Worker/Archive" service

# Docker Compose
All services are distributed among four docker containers. To make them work we need use the following command to start all processes:
```
$ docker-compose up -d
Creating whole_project_rabbitmq_1 ... done
Creating whole_project_server_1   ... done
Creating whole_project_worker_1   ... done
Creating whole_project_archive_1  ... done
```

After a while we can see all four processes running
```
$ docker-compose ps
Name                        Command                       State                                                                    Ports                                     
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
whole_project_archive_1    python3 archive.py               Up                                                                                                                                             
whole_project_rabbitmq_1   docker-entrypoint.sh rabbi ...   Up (health: starting)   15671/tcp, 0.0.0.0:15672->15672/tcp,:::15672->15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp,                                
                                                                                    0.0.0.0:5672->5672/tcp,:::5672->5672/tcp                                                                               
whole_project_server_1     python3 server.py                Up                      0.0.0.0:5000->5000/tcp,:::5000->5000/tcp                                                                               
whole_project_worker_1     python3 worker.py                Up
```

# Send request
To get a task from the dictionary we'll use the HTTP's GET method:
```
$ curl -i http://localhost:5000/myproject/v1.0/tasks/3

HTTP/1.0 200 OK
**Content-Type**: text/html; charset=utf-8
**Content-Length**: 120
**Server**: Werkzeug/2.0.1 Python/3.6.9
**Date**: Thu, 07 Oct 2021 00:02:11 GMT

sent 3
b'{"task": {"id": 3, "title": "Compete on Codeforces", "description": "Get to the first place", "done": false}}'
```

*There'll be more request types in the near future*
