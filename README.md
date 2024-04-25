# project3_se

## Instructions to Run:

docker network create micro_network

## In every micro-services run
docker-compose -f docker-compose.yml build
docker images

docker-compose -f docker-compose.yml up -d
docker ps -a

for service in corder-service cproduct-service cuser-service;
do 
 docker exec -it $service flask db init
 docker exec -it $service flask db migrate
 docker exec -it $service flask db upgrade
done

http://localhost:5000/register


## Teardown of Microservices
1. Perform the following steps to teardown the microservices environment:

for container in cuser-service cproduct-service corder-service cproduct_dbase cfrontend-app cuser_dbase corder_dbase;
do
 docker stop $container
 docker rm $container
done


2. Remove the container volumes

for vol in frontend_orderdb_vol frontend_productdb_vol frontend_userdb_vol;
do
 docker volume rm $vol
done


3. Remove the container network

docker network rm micro_network
