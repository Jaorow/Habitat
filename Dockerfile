# Use the official Python image
FROM python:3.10-slim AS backend

# Set the working directory for the backend
WORKDIR /app

# Copy only the backend code and dependencies
COPY backend/requirements.txt /app/
COPY backend/ .

# Use a Node.js image to build the React frontend
FROM node:18 AS frontend

# Set the working directory for the frontend
WORKDIR /frontend

# Copy the React app code
COPY frontend/package.json frontend/package-lock.json /frontend/

# Set environment variables for the React app to hit compiled endpoints
ENV REACT_APP_API_ENDPOINT=""
# Install dependencies and build the React app
RUN npm install
COPY frontend/ /frontend/
RUN npm run build


# Final stage: Combine backend and frontend
FROM python:3.10-slim

# Set the working directory for the final app
WORKDIR /app

# Copy the backend code
COPY --from=backend /app /app

# Copy the built React frontend into the backend's static folder
# Dont need to copy build as we auto build into said folder
# COPY --from=frontend /frontend/build /app/frontend_build

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8080

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
