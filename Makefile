db:
	pipenv run python watchlist/manage.py makemigrations
	pipenv run python watchlist/manage.py migrate

run:
#	cd watchlist/
#	pwd
	pipenv run ./watchlist/manage.py runserver

install:
	pip install pipenv 
	pipenv --python 3.7 
	pipenv install django
	pipenv install requests
	pipenv install huey
	pipenv install ipdb --dev
	make db
#	make run

test:
	pipenv run python watchlist/manage.py test watchlist

shell:
	python watchlist/manage.py shell


