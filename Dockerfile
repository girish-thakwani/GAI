# Multi-stage Dockerfile
# Stage 1: Build frontend
FROM node:18-slim AS frontend

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ .

# Ensure node_modules binaries are executable
RUN chmod -R +x node_modules/.bin

# Build the application
RUN npm run build

# Stage 2: Backend
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
# Remove pywinpty (Windows-only, causes build errors in Linux Docker)
RUN grep -v pywinpty requirements.txt > requirements-clean.txt && \
    pip install --no-cache-dir -r requirements-clean.txt

# Copy backend source code
COPY backend/ .

# Copy built frontend from previous stage
COPY --from=frontend /app/dist ./static

# Expose port
EXPOSE 8000

# Run the application
CMD ["sh", "-lc", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]