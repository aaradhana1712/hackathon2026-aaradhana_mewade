# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create an empty .env file if it doesn't exist (User should provide their own or we use Mock)
RUN touch .env

# Run main.py when the container launches
CMD ["python", "main.py"]
