<div align='center'>
  
# Scalable Proxy Server

[![forthebadge](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com)

</div>

A proxy server that can be hosted easily anywhere with a dashboard to monitor all the requests and their statuses. The proxy server would be scalable and load balancers would be used. This was done to try building building scalable applications and learn many tools.

## Server

* A flask application with an endpoint to handle the incoming requests
* Forward all the requests and fetch appropriate responses
* Scalable as there can be huge number of requests at the same time based on CPU utilization
* Load balances across the various nodes

## Monitor

* Elastic Stack comprising of Elastic Search, Logstash and Kibana is used
* All the incoming requests are saved to Elastic Search
* The logs of the flask server are recorded in Logstash
* Kibana dashboard is used for keeping track of the logs and requests

## Setup

Setting up Elastic Stack-Monitor
```
cd Monitor/
docker-compose up
```

Setting up Flask-Server
```
cd Server/
docker build . -t flask-proxy-server
```

Running the kubernetes nodes and autoscaling
```
sudo minikube start --vm-driver=none
kubectl apply -f Server/deployment.yaml
kubectl autoscale deployment flask-proxy-server --cpu-percent=50 --min=1 --max=10
```

`python3 proxy.py` A script for simulate high load on the server 

## Contributing

Open to enhancements & bug-fixes
