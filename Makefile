APP_TAG := loperd/report-tg-channels:latest
USER := loperd

build:
	docker build -t $(APP_TAG) .

push:
	docker push $(APP_TAG)

login:
	docker login -u $(USER)