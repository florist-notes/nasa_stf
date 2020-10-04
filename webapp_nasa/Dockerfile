FROM python:3.7-slim
#RUN apt-get update && apt-get install -y gcc build-essential curl cron

# All the services that use this image should expect common to be in /usr/app/common
WORKDIR /usr/app

# Service specific requirements
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . .

#RUN chown -R nobody: .
#USER nobody
