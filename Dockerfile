FROM ubuntu:latest
LABEL authors="noah"

# syntax=docker/dockerfile:1
FROM python:3.10-alpine

# Set the working directory inside the container
WORKDIR /code

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Install dependencies
RUN apk add --no-cache musl-dev libffi-dev

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the Flask application
CMD ["python", "run.py"]
