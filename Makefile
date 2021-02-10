db:
	pipenv run python watchlist/manage.py makemigrations
	pipenv run python watchlist/manage.py migrate

# run:
#	cd watchlist
#	pipenv run python manage.py runserver &&	pipenv run python manage.py run_huey

install:
	pip install pipenv 
	pipenv --python 3.7 
	pipenv install django
	pipenv install requests
	pipenv install huey
	pipenv install ipdb --dev
	make db
#	make run




