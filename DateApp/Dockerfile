# Use latest python image
FROM python:3.8.4-slim

# Meta-data
LABEL maintainer = "Aaron Bushnell" \
      name = "DateApp" \
      verion = "0.1"

# Set working directory and copy code
WORKDIR /dateapp
ADD . /dateapp

# Pip install requirements
RUN apt update
RUN apt install -y git
RUN apt install -y gcc
RUN pip install -r requirements.txt

# Specify entry point for gunicorn
ENTRYPOINT ["bash", "./gunicorn.sh"]

# Run cleaning script in Docker
#CMD ["python", "run.py"]
