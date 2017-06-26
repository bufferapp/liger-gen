NAME := bufferapp/liger-gen

.PHONY: all
all: run

.PHONY: build
build:
	docker build -t $(NAME) .

.PHONY: run
run:
	docker run -it --rm --env-file .env $(NAME)


.PHONY: dev
dev:
	docker run -it --rm --env-file .env -v $(PWD):/usr/src/app --entrypoint /bin/bash $(NAME)
