# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    tcl-dev \
    tk-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

# Create a non-root user
RUN useradd -m -u 1000 tracker && chown -R tracker:tracker /app
USER tracker

# Expose port (if needed for any web interface)
EXPOSE 8080

# Run the application
CMD ["python", "src/main.py"]

