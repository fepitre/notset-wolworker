FROM python:3.8-alpine
MAINTAINER Frédéric Pierret <frederic.pierret@qubes-os.org>

EXPOSE 5000

WORKDIR /home/user
VOLUME ["/home/user"]
COPY . /home/user

ENV FLASK_DEBUG 1
ENV FLASK_APP wolworker.py

RUN pip3 install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
