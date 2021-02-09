db:
	pipenv run python watchlist/manage.py makemigrations
	pipenv run python watchlist/manage.py migrate


install:
	pip install pipenv 
	pipenv --python 3.7 
	#pipenv shell 
	pipenv install django
	pipenv install requests
	pipenv install celery
	pipenv install ipdb --dev
	make db



