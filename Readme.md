# Scalable Proxy Server

A proxy server that can be hosted easily anywhere with a dashboard to monitor all the requests and their statuses. The proxy server would be scalable and load balancers would be used. This was done to try building building scalable applications and learn many tools.

## Server

* Forward all the requests and fetch appropriate responses
* Log the incoming requests
* Scalable as there can be huge number of requests at the same time
* Load balance CPU utilization

## Monitor

* Elastic Stack

```
cd Monitor/
docker-compose up
```

```
cd Server/
docker build . -t flask-proxy-server
```

```
sudo minikube start --vm-driver=none
kubectl apply -f Server/deployment.yaml
kubectl autoscale deployment flask-proxy-server --cpu-percent=50 --min=1 --max=10
```


