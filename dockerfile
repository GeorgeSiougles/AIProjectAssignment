# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the environment file to the working directory in the container
COPY .env.local /app/.env.local

# Install any needed packages specified in requirements.txt
# --no-cache-dir prevents the caching of package files to reduce image size
RUN pip install --no-cache-dir -r requirements.txt 

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to ensure stdout and stderr are sent straight to terminal (useful for debugging)
ENV PYTHONUNBUFFERED=1

# Run uvicorn server with live-reload enabled
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
