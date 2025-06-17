FROM python:3.12-slim
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy in the source code
COPY . .
EXPOSE 8000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["python", "manage.py", "runserver", "0.0.0.0", "--port", "8000"]