set container_name=fastApi
set image_name=biber
docker stop %container_name%
docker rm %container_name%
docker rmi %image_name%

docker builder builder prune 

docker build -t %image_name% .
docker run -d --name %container_name% -p 10100:10100 %image_name%

for /f "tokens=1" %%a in ('docker ps ^| findstr biber') do set image_id=%%a
docker exec -it  %image_id%  /bin/bash -c "pytest"