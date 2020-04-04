# multa-metrics-agent

- Includes agent code that will deploy in devices. Initially as a Docker container that can be deployed in any Unix-like OS, needs to provide:

## Dockerfile
- Allows to build your own custom agent with the commands:

`export VERSION=### && make build && make tag`

## docker run 
- Allows to run Multa Metrics Agent using docker CLI using the command:

``
docker run -e DEVICE_NAME=${DEVICE_NAME}
  -e DEVICE_CONFIGURATION_URL=https://cvm-agent.dev.multa.io/multa-agent/ 
  --net=host --restart always --privileged -d --name multa-agent 
  112646120612.dkr.ecr.us-east-1.amazonaws.com/multa-agent:0.0.1
``

## docker-compose.yml file 
- Allows to run Multa Metrics Agent using docker-compose command: ``docker-compose up``

## Other deployment methods

## Next features
- Will be updated later to include AWS IoT Device Defender
- Can be later updated ot include AWS Greengrass and make it a truly reporting agent/gateway
