build:
	docker compose up --build -d --remove-orphans


up:
	docker compose up -d


down:
	docker compose down


show-logs:
	docker compose logs


show-logs-api:
	docker compose logs bot
