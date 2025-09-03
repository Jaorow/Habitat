# Stage 1: Build React frontend
FROM node:18 AS frontend

WORKDIR /frontend

# Copy frontend code
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: Build Python backend
FROM python:3.10-slim AS backend

WORKDIR /app

# Copy backend requirements and code
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

# Copy the built frontend into backend static folder
COPY --from=frontend /frontend/dist /app/dist

# Expose port FastAPI will listen on
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]