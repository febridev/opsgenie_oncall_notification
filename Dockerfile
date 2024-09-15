FROM python:3.12-slim

# Install cron and any other necessary packages
RUN apt-get update && apt-get install -y cron tzdata

# Set the timezone to Asia/Jakarta
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install PDM
RUN pip install -U pdm

# COPY all Files project 
COPY pyproject.toml pdm.lock README.md .env /project/
COPY src/ /project/src

# SET WORKDIR PROJECT
WORKDIR /project

# INSTALL all Packages Dependency
RUN pdm install --check --prod --no-editable


# CRONTAB
COPY run.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/run.sh

# CREATE LOG FILE FOR CRON
RUN touch /var/log/cron.log

# CREATE SPECIFIC CRON
RUN echo "0 8 * * 1-5 /usr/local/bin/run.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job
RUN crontab /etc/cron.d/my-cron-job

# SET CONTAINER RUN CRON
CMD ["cron","-f", "-l", "2"]

