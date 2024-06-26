# Dockerfile
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Set work directory
WORKDIR /code


# Copy project
COPY . /code/

EXPOSE 8000

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN python -m pip install --upgrade pip

# Install dependencies from the requirements.txt file to ensure our Python environment is ready
RUN pip install -r requirements.txt

# Run the Django server using gunicorn
CMD ["gunicorn", "BoostApp.wsgi:application", "--bind", "0.0.0.0:8000"]