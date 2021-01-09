# run only after auth and social-network services are loaded
run-bot:
	docker-compose run automated-bot python main.py

up:
	docker-compose down
	docker-compose up --build

down:
	docker-compose down

# run auth service management command
run-auth:
	docker-compose exec auth-service python manage.py $(command)

# run social network service management command
run-sn:
	docker-compose exec social-network python manage.py $(command)
