# from official python image
FROM python:3.13.2-slim

# Install wget
RUN apt-get update && apt-get install -y wget net-tools && rm -rf /var/lib/apt/lists/*

# working directory
WORKDIR /app

# install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app/

# Expose port for FastAPI app
EXPOSE 8000

# Launch FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
