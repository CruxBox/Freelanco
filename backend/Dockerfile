FROM python:3.6

RUN mkdir /freelanco

COPY ./requirements.txt /freelanco/requirements.txt

WORKDIR /freelanco

RUN pip3 install -r requirements.txt

COPY . /freelanco/

RUN chmod +x /freelanco/docker-entrypoint.sh

ENTRYPOINT ["bash","/freelanco/docker-entrypoint.sh"]
