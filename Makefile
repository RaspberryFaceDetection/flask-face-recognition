build:
	docker build -t flask-face-identification:latest ./

up:
	docker-compose up -d flask

stop:
	docker-compose stop flask

rm:
	docker-compose rm -f flask

down: stop rm

restart: down build up

clean:
	docker rmi -f $$(docker images -f "dangling=true" -q) || true

bash:
	docker exec -it flask-face-identification_flask_1 bash


