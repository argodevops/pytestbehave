FROM selenium/standalone-chrome:105.0

USER root

RUN curl -s https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl -s https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update -y && apt-get install -y python3-tk python3-pip && apt-get install -y python3-hamcrest
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 && ACCEPT_EULA=Y apt-get install -y mssql-tools18 && apt-get install -y unixodbc-dev
COPY resolved.conf /etc/systemd/resolved.conf

WORKDIR /src

COPY . .

RUN pip3 install -Iv -r requirements.txt
