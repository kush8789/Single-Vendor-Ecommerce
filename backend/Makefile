.PHONY: env
env:
	ecommerce_env/Scripts/activate 

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: run-server
run-server:
	python manage.py runserver

.PHONY: superuser
superuser:
	python manage.py createsuperuser