app:
	poetry run streamlit run confluence_chat/app.py --server.runOnSave=true

docker-build:
	docker compose --profile server build

docker-run:
	# Runs all services within Docker containers
	docker compose --profile server up
