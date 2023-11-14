#!/bin/bash


container_name=fastApi
image_name=biber
docker stop $container_name
docker rm $container_name
docker rmi $image_name

docker builder builder prune # for cache

docker build -t $image_name .
docker run -d --name $container_name -p 10100:10100 $image_name


if ["$1" = "build"]
then
    ## testing
    img_id=$(docker ps | grep biber | awk '{print $1}')
    docker exec -i $img_id /bin/bash -c "pytest"
fi
