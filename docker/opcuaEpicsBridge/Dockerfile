FROM python:3.8.7

RUN apt-get update && apt-get install -y build-essential python3-dev python2.7-dev \
    libldap2-dev libsasl2-dev ldap-utils tox \
    lcov valgrind
ADD ./opcuaEpicsBridge/requirements.txt /bridge/requirements.txt
WORKDIR /bridge

RUN pip install -r requirements.txt


ENV EPICS_BASE=/epics/base/

WORKDIR /epics

RUN wget https://epics.anl.gov/download/base/base-3.15.6.tar.gz
RUN tar -xvf base-3.15.6.tar.gz
RUN ln -s /epics/base-3.15.6 /epics/base
WORKDIR /epics/base
RUN make
WORKDIR /epics


ADD ./opcuaEpicsBridge /bridge
WORKDIR /bridge



ENV EPICS_CA_ADDR_LIST="0.0.0.0:8001 0.0.0.0:8002 0.0.0.0:8003 0.0.0.0:8004"
ENV PYEPICS_LIBCA=/epics/base/lib/linux-x86_64/libca.so

ENV PATH="/epics/base/bin/linux-x86_64/:${PATH}"




CMD python bridge.py
EXPOSE  5000 5001 5064 5065 8001 27017
