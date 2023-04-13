FROM python:3.8.7

RUN apt-get update && apt-get install -y build-essential python3-dev python2.7-dev \
    libldap2-dev libsasl2-dev ldap-utils tox \
    lcov valgrind
ADD ./opcuaSimple/requirements.txt /opcuaSimple/requirements.txt
WORKDIR /opcuaSimple

RUN pip install -r requirements.txt
ADD ./opcuaSimple /opcuaSimple

CMD python client-minimal.py
EXPOSE  4840
