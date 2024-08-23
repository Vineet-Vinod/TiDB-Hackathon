FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install git and other dependencies
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory into the container at /app/src
COPY src/ ./src

# Set Flask App Configs
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

WORKDIR /app/src
CMD ["flask", "run"]