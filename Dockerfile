# Use official lightweight Python image with TensorFlow
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set Hugging Face cache directory
ENV HF_HOME=/app/hf_cache
RUN mkdir -p /app/hf_cache && chmod -R 777 /app/hf_cache

# Copy requirement definitions
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Expose the port your Flask app runs on
EXPOSE 7860

# Run the Flask app
CMD ["python", "app.py"]
