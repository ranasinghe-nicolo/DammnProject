# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8080 to allow external access
EXPOSE 8080

# Run the Python HTTP server
CMD ["python3", "-m", "http.server", "8080"]
