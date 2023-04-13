FROM python:3.8.7

# RUN apt-get update && apt-get install -y build-essential python3-dev python2.7-dev \
#     libldap2-dev libsasl2-dev ldap-utils tox \
#     lcov valgrind
ADD ./opcuaEpicsBridge/requirements.txt /bridge/requirements.txt
WORKDIR /bridge

RUN pip install -r requirements.txt

ADD ./opcuaEpicsBridge /bridge
ADD ./dbtoolspy/dbtoolspy /bridge/dbtoolspy

WORKDIR /bridge

CMD python bridge.py

