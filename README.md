# 1 Installation
This system has been containerized with Docker.

It is advised to only use the containerized version with a Linux environment. (See the FAQ section on other operating systems).


Prerequisites: git, latest version of docker-ce and docker compose 

( At the time of writing the system used Docker V23.0.3 and docker compose V2.17.2 )

To install docker-ce  and docker compose on Unbuntu follow:

https://docs.docker.com/engine/install/ubuntu/

It is advised to the follow the Post Installation steps for Linux:

https://docs.docker.com/engine/install/linux-postinstall/


1st clone this repo:

```bash
git clone --recurse-submodules git@github.com:React-Automation-Studio/OPCUA-EPICS-BRIDGE.git

```


# 2 Launching the Docker compose files
The systems uses Docker to create isolated production and development environments. There are several docker-compose configuration files.


Firstly bring up the demo OPCUA server in a terminal.

```bash
docker compose -f docker-compose-simple.yml up --build
```

Then bring up the demo OPCUA-EPICS bridge with:

```bash
docker compose  up --build
```
or
```bash
docker compose -f docker-compose.yml up --build
```


# 38 Contact

Contact us at Github Discussions: https://github.com/React-Automation-Studio/React-Automation-Studio/discussions