# Multi-stage Dockerfile
# Stage 1: Build frontend
FROM node:18-slim AS frontend

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies with proper permissions
RUN npm ci && npm install

# Copy source code
COPY frontend/ .

# Build the application
RUN npm run build

# Stage 2: Backend
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Copy built frontend from previous stage
COPY --from=frontend /app/dist ./static

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]