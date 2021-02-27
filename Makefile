db:
	pipenv run python watchlist/manage.py makemigrations
	pipenv run python watchlist/manage.py migrate

run-django:
	pipenv run django

run-huey:
	pipenv run django

run:
	pipenv run django & \
	pipenv run huey &

stop:
	pipenv run stop

install:
	pip install pipenv 
	pipenv --python 3.7 
	pipenv install
#	pipenv install django
#	pipenv install requests
#	pipenv install huey
#	pipenv install ipdb --dev
	make db

test:
	pipenv run test

shell:
	python watchlist/manage.py shell

docker:
	pipenv 
