up:
	docker-compose up --build -d

down:
	docker-compose down

test:
	pytest tests/ -v