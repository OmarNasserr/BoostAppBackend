# Dockerfile
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV PORT 8000

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

# Copy entrypoint script
COPY entrypoint.sh /code/entrypoint.sh

# Make entrypoint script executable
RUN chmod +x /code/entrypoint.sh

EXPOSE 8000

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN python -m pip install --upgrade pip

# Install dependencies from the requirements.txt file to ensure our Python environment is ready
RUN pip install -r requirements.txt

# Set the entrypoint script
ENTRYPOINT ["/code/entrypoint.sh"]
