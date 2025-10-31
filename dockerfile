# Base image to use, fewer included packages, because we need to keep image lighter for AI_Model and database
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

    #First doesnt create .pyc files
    #Second Pip dont cache downloaded packages

# All commands about to happen happens in this directory
WORKDIR /app

# Linux commads, for upgrade and install, flags first mean yes and second not to install "recommended dependencies packages" making it lighter. 
# Source: "https://ubuntu.com/blog/we-reduced-our-docker-images-by-60-with-no-install-recommends"
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*
# Needed if pip-packages needs to be converted and git, because open_clip_torch gets model weigths from Github
# Deletes caches, for again making image lighter
# Copying file to image, so pip can install
COPY requirements.txt .

# install and upgrade pip and then install requirements file
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# copy app to image
COPY app ./app

# copy AI_MODEL to image
COPY AI_Model ./AI_Model

# making folder for save_upload to save pictures, -p flag creates them if they do not already exist.
RUN mkdir -p /app/uploads

# Using uvicorn to start application, listening everywhere and use Render given port or if not given then port 8000
ENV PORT=8000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]