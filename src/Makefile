

# ### Docker management commands 
 
docker-up: 
	docker compose -p code_manager -f production.yml up --build -d --remove-orphans 

docker-down: 
	docker compose -p code_manager -f production.yml down

docker-down-v: 
	docker compose -p code_manager -f production.yml down -v

docker-logs: 
	docker compose -p code_manager -f production.yml logs 

docker-logs-code-manager: 
	docker compose -p code_manager -f production.yml logs code-manager

docker-restart-code-manager: 
	docker compose -p code_manager -f production.yml restart code-manager

docker-exec-code-manager: 
	docker compose -p code_manager -f production.yml exec code-manager /bin/bash 

# ## 

# ### Other Services  (In production, nginx proxy manager is used, nginx here is only to test production locally)
docker-restart-nginx: 
	docker compose -p code_manager -f production.yml restart nginx 

docker-restart-redis: 
	docker compose -p code_manager -f production.yml restart codemanager-cache-redis

docker-restart-postgres: 
	docker compose -p code_manager -f production.yml restart postgres

# ### Docker Volume and Postgres Database 

docker-volume: 
	docker volume inspect src_dev_postgres_data

docker-exec-postgres: 
	docker compose -p code_manager -f production.yml exec postgres /bin/bash 

algocode-questions-db: 
	docker compose -p code_manager -f production.yml exec postgres psql --username="$(POSTGRES_USER)" --dbname="$(POSTGRES_DB)" 

# ## 




# ### Services logs commands 

docker-logs-redis:
	docker compose -p code_manager -f production.yml logs codemanager-cache-redis

docker-logs-postgres: 
	docker compose -p code_manager -f production.yml logs postgres

# ## 


# ### Django Commands

makemigrations: 
	docker compose -p code_manager -f production.yml run --rm code-manager python manage.py makemigrations

migrate: 
	docker compose -p code_manager -f production.yml run --rm code-manager python manage.py migrate

collectstatic: 
	docker compose -p code_manager -f production.yml run --rm code-manager python manage.py collectstatic --no-input --clear 

superuser: 
	docker compose -p code_manager -f production.yml run --rm code-manager python manage.py createsuperuser 

# ## 




# ### Pytest Commands
pytest-no-wrn-codecov:
	docker compose -p code_manager -f production.yml run --rm code-manager pytest -p no:warnigns --cov=. -v  

pytest-no-wrn-codecov-html:
	docker compose -p code_manager -f production.yml run --rm code-manager pytest -p no:warnigns --cov=. --cov-report html



# ### Other Tools for Formatting 

flake8: 
	docker compose -p code_manager -f production.yml exec code-manager flake8 . 

black-check: 
	docker compose -p code_manager -f production.yml exec code-manager black --check --exclude=migrations . 

black-diff: 
	docker compose -p code_manager -f production.yml exec code-manager black --diff --exclude=migrations . 

black: 
	docker compose -p code_manager -f production.yml exec code-manager black --exclude=migrations . 

isort-check: 
	docker compose -p code_manager -f production.yml exec code-manager isort . --check-only --skip venv --skip migrations 

isort-diff: 
	docker compose -p code_manager -f production.yml exec code-manager isort . --diff --skip venv --skip migrations

isort: 
	docker compose -p code_manager -f production.yml exec code-manager isort . --skip venv --skip migrations

# ## 