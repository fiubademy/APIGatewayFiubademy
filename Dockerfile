FROM ubuntu
WORKDIR /app
RUN apt-get -y update 
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
EXPOSE 8000
RUN mkdir gateway
COPY Commands.sh /app/
COPY gateway/. /app/gateway
CMD ./Commands.sh

