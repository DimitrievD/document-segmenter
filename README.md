

This project uses a YOLOv8 segmentation model served by a Python Flask API to automatically detect and extract individual documents from a single image. A modern React front-end provides a user-friendly interface for uploading images and viewing the results.

## 🚀 Key Features

-   **AI-Powered Backend**: Utilizes a powerful YOLO model for accurate document segmentation.
-   **RESTful API**: Python/Flask backend serves the model and processes images.
-   **Interactive Frontend**: React app with drag-and-drop and file browser for image uploads.
-   **Cross-Platform**: Includes setup and run scripts for both Windows and Linux/macOS.
-   **Easy Setup**: One-command installation for all dependencies (Python & Node.js).
-   **Simple Launch**: One command to start both the backend API and the frontend server concurrently.

## 🏛️ Project Architecture

```[User] <--> [Browser: React Frontend] <--> [API: Python/Flask Backend] <--> [YOLOv8 Model]
```

## ✅ Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python 3.9+** (ensure it's added to your system's PATH).
-   **Node.js v16+** and **npm** (Node Package Manager).
-   **Git** (for cloning the repository).
-   **(Optional)** An NVIDIA GPU with CUDA drivers for GPU acceleration with PyTorch.

---

## ⚡ Quick Start

This is the fastest way to get the entire application running.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/DimitrievD/document-segmenter.git
    cd document_detector
    ```

2.  **Run the Installation Script**
    This will create a Python virtual environment, install all backend and frontend dependencies automatically.

    -   **On Windows (PowerShell or CMD):**
        ```powershell
        .\install.bat
        ```
    -   **On Linux or macOS:**
        ```bash
        # First, make the script executable
        chmod +x install.sh
        
        # Then, run it
        ./install.sh
        ```

3.  **Run the Application Start Script**
    This will launch both the Flask API and the React development server in separate terminal windows.

    -   **On Windows:**
        ```powershell
        .\start.bat
        ```
    -   **On Linux or macOS:**
        ```bash
        ./start.sh
        ```

4.  **Access the Application**
    -   Open your web browser and navigate to the frontend: **`http://localhost:3000`**
    -   The backend API will be running at: `http://localhost:5000`

    To stop the servers on Linux/macOS, press `Ctrl + C` in the terminal where you ran `start.sh`. On Windows, close the two new terminal windows that opened.

---

## 🛠️ Manual Setup & Execution

If you prefer to set up and run the services manually, follow these steps.

### Backend Setup (Flask API)

1.  **Create and Activate Virtual Environment:**
    ```powershell
    # Create the virtual environment
    python -m venv venv

    # Activate it (Windows PowerShell)
    .\venv\Scripts\Activate.ps1
    
    # Or (Linux/macOS)
    source venv/bin/activate
    ```

2.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Frontend Setup (React App)

1.  **Navigate to the Frontend Directory:**
    ```bash
    cd document-processor-frontend
    ```

2.  **Install Node.js Dependencies:**
    ```bash
    npm install
    ```

### Running Manually

You will need **two separate terminals**.

-   **In Terminal 1 (Project Root), run the Backend:**
    ```bash
    # Make sure your venv is active
    python app.py
    ```

-   **In Terminal 2, run the Frontend:**
    ```bash
    # Navigate to the frontend directory
    cd document-processor-frontend

    # Start the React app
    npm start
    ```

---

## 📁 Project Structure

```
/document_detector
│
├── 📜 app.py                      # Main Flask API file
├── 📜 requirements.txt             # Python dependencies
│
├── 📂 document-processor-frontend/ # React frontend application
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── 📂 venv/                         # Python virtual environment (created by script)
│
├── 📜 install.bat                  # Windows installation script
├── 📜 install.sh                   # Linux/macOS installation script
├── 📜 start.bat                    # Windows start script
└── 📜 start.sh                     # Linux/macOS start script
```

---

##  Troubleshooting

-   **CORS Error in Browser Console**: This means the frontend cannot communicate with the backend. Ensure you have installed and configured `flask-cors` in your `app.py`.
-   **PowerShell Script Execution Blocked**: If `.\venv\Scripts\Activate.ps1` is blocked, run PowerShell as an Administrator and execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
-   **`pip install` Fails**: Some packages may require C++ build tools. On Windows, you might need to install "Microsoft C++ Build Tools" from the Visual Studio Installer.
-   **Port Conflict**: If port 5000 or 3000 is in use, the application may fail to start. You can configure the port in the `app.py` script (for Flask) or by modifying the `npm start` script (for React).
```
