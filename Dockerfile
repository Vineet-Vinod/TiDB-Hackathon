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

# Expose the port that the Flask app will run on
EXPOSE 5000
CMD ["python", "src/app.py"]