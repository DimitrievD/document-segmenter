#!/bin/bash

# Function to clean up background processes on exit
cleanup() {
    echo -e "\n\nShutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID
    echo "Servers stopped."
    exit
}

# Trap SIGINT (Ctrl+C) and call the cleanup function
trap cleanup SIGINT

echo "=============================================="
echo "== Starting Document Detector Application... =="
echo "=============================================="
echo

# Start the Flask Backend in the background
echo "-> Starting Flask API Backend..."
(source venv/bin/activate && python app.py) &
BACKEND_PID=$! # Get the Process ID of the last command run in the background
echo "   Backend started with PID: $BACKEND_PID"
echo

# Start the React Frontend in the background
echo "-> Starting React Frontend..."
(cd document-processor-frontend && npm start) &
FRONTEND_PID=$!
echo "   Frontend started with PID: $FRONTEND_PID"
echo

echo "=========================================================="
echo "✅ Application is running!"
echo "   - Frontend available at: http://localhost:3000"
echo "   - Backend API running at: http://localhost:5000"
echo
echo "Press Ctrl+C to shut down both servers gracefully."
echo "=========================================================="

# Wait for background processes to finish (which they won't, until we kill them)
wait