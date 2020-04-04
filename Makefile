.PHONY: login build tag deploy
.DEFAULT_GOAL := help

SHELL := /bin/bash
LOGIN :=
PROJECT := multa-agent
REPO := 112646120612.dkr.ecr.us-east-1.amazonaws.com

login:
	$(shell aws ecr get-login --no-include-email --region us-east-1)

build:
	docker build -t ${PROJECT} -f etc/docker/Dockerfile .

tag:
	docker tag ${PROJECT}:latest ${REPO}/${PROJECT}:${VERSION}

push:
	docker push ${REPO}/${PROJECT}:${VERSION}