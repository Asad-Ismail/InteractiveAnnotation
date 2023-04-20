#!/bin/bash

# Change to the backend directory and install requirements
cd backend
echo "Installing backend requirements..."
pip install -r requirements.txt

# Run the backend application in the background
echo "Starting backend server..."
./run_app.sh &

# Change to the frontend directory
cd ../frontend/annotation-tool

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Run the frontend application
echo "Starting frontend server..."
npm run serve
