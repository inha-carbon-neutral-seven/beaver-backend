#!/bin/bash

container_name=fastApi
image_name=biber
docker stop $container_name
docker rm $container_name
docker rmi $image_name

docker builder builder prune # for cache

docker build -t $image_name .
docker run -d --name $container_name -p 10100:10100 $image_name
