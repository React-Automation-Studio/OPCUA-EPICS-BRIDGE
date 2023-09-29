# Introduction 

OPC UA is a service-orientated communication architecture  that supports platform-independent, data exchange between
embedded microcontrollers, PLCs or PCs and cloudbased infrastructure. This makes OPC UA ideal for developing
manufacturer independent communication to vendor specific PLCs, for example. With this in mind, we present
an OPC UA to EPICS bridge that has been containerized with Docker to provide a microservice for communicating
between EPICS and OPC UA variables.

<img src="./img/microservice.PNG" alt="drawing" width="90%"/>


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


Firstly bring up the demo unsecure OPCUA server in a terminal.

```bash
docker compose -f git@github.com:React-Automation-Studio/OPCUA-EPICS-BRIDGE.git up --build
```

This will load an opcua  server test variables and the Epics bridge with variables declare in the db/test.tb

The Epics process variables can then be access via any Epics client such as caput, caget and cainfo for example or through a the GUI available at:

https://github.com/wduckitt/React-Automation-Studio-Example-OPCUA.git




# 38 Contact

Contact us at Github Discussions: https://github.com/React-Automation-Studio/React-Automation-Studio/discussions
