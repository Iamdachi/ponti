# Use an official Python runtime as a parent image, using a 'slim' base for smaller image size.
FROM python:3.14-slim

# Set environment variables to prevent Python from writing .pyc files and unbuffer logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies before copying the rest of the code for better Docker caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code into the container
COPY . /app/

# Expose the port the Django development server will run on
EXPOSE 8000

# Run the Django development server on container startup
# This command is for development. In production, you'd use Gunicorn/uWSGI.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]