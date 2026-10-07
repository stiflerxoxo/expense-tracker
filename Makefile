.PHONY: up down logs test build clean

up:      ## build and start everything
	docker compose up -d --build
down:    ## stop containers
	docker compose down
logs:
	docker compose logs -f
test:    ## run backend unit tests
	cd backend && pip install -q -r requirements.txt && pytest -q
clean:   ## stop and delete database volume
	docker compose down -v
