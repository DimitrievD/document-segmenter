#!/bin/bash

cleanup() {
    echo -e "\n\nShutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID
    echo "Servers stopped."
    exit
}

trap cleanup SIGINT

echo "=============================================="
echo "== Starting Document Detector App...        =="
echo "=============================================="
echo

cd ..

echo "-> Starting Flask API Backend..."
(source venv_app/bin/activate && python app/app.py) &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo

echo "-> Starting React Frontend..."
(cd document-processor-frontend && npm start) &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo

echo "=========================================================="
echo "✅ Application is running!"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend: http://localhost:5000"
echo
echo "Press Ctrl+C to stop."
echo "=========================================================="

wait
