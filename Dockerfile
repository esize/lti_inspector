#FROM python:2
FROM amazonlinux
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir /code/logs
WORKDIR /code
RUN yum install python27-pip -y
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN chmod a+x /code/docker-entrypoint.sh
EXPOSE 8000
