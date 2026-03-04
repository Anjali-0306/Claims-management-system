#Base image
FROM python:3.11-slim

#Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Create non-root user
RUN addgroup --system appgroup && adduser --system --group appuser


#set working directory
WORKDIR /app
#Install System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
#Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy Project
COPY . .

#Change ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

#Run with Gunicorn
CMD ["python", "-m", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

