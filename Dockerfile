FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["monailabel", "start_server", "--app", "apps/radiology", "--studies", "datasets/", "--conf", "models", "airway_segmentation"]