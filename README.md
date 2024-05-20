# testvm
docker stop $(docker ps -q)
docker container rm $(docker ps -a -q)
docker rmi $(docker images -q) --force
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q)