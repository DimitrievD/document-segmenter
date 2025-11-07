import React, { useState, useCallback, useRef } from 'react';
import './App.css';
import { ReactComponent as UploadIcon } from './upload-icon.svg'; // We'll create this icon file next

function App() {
    const [documents, setDocuments] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isDragActive, setIsDragActive] = useState(false);
    const fileInputRef = useRef(null); // Create a ref for the file input

    // This function handles the API call
    const processImage = async (file) => {
        if (!file || !file.type.startsWith('image/')) {
            setError("Please select a valid image file (PNG, JPG).");
            return;
        }

        setIsLoading(true);
        setError(null);
        setDocuments([]);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/segment', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: `Server responded with status: ${response.status}` }));
                throw new Error(errorData.message);
            }

            const result = await response.json();

            if (result.status === 'success') {
                setDocuments(result.documents || []);
                if (result.documents.length === 0) {
                    setError("No documents were detected in the uploaded image.");
                }
            } else {
                throw new Error(result.message || 'An unknown error occurred during processing.');
            }

        } catch (err) {
            console.error("Processing error:", err);
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    // --- NEW: Function to clear results ---
    const handleClear = () => {
        setDocuments([]);
        setError(null);
        // Also reset the file input so the same file can be re-uploaded
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    // --- Event Handlers for Drag and Drop ---
    const handleDrag = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setIsDragActive(true);
        } else if (e.type === "dragleave") {
            setIsDragActive(false);
        }
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            processImage(e.dataTransfer.files[0]);
        }
    }, []);
    
    // --- Event Handler for File Browser ---
    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            processImage(e.target.files[0]);
        }
    };
    
    const triggerFileSelect = () => {
        fileInputRef.current.click();
    };

    // Determine if the results area should be shown
    const showResultsArea = documents.length > 0 || error || isLoading;

    return (
        <div className="container">
            <header className="header">
                <h1>Document Segmentation AI</h1>
                <p>Upload an image to automatically identify and extract individual documents.</p>
            </header>

            <main>
                <input
                    type="file"
                    id="fileInput"
                    ref={fileInputRef} // Attach the ref
                    accept="image/png, image/jpeg"
                    onChange={handleFileChange}
                    hidden
                />
                <div
                    className={`drop-zone ${isDragActive ? 'drag-active' : ''}`}
                    onDragEnter={handleDrag}
                    onDragOver={handleDrag}
                    onDragLeave={handleDrag}
                    onDrop={handleDrop}
                    onClick={triggerFileSelect} // Allow clicking the whole box
                >
                    <UploadIcon className="upload-icon" />
                    <p>
                        Drag & Drop Your Image Here or <span>Browse Files</span>
                    </p>
                </div>

                {showResultsArea && (
                    <div className="results-section">
                        <div className="results-header">
                            <h2>Results</h2>
                            {(documents.length > 0 || error) && !isLoading && (
                                <button onClick={handleClear} className="clear-btn">
                                    Clear
                                </button>
                            )}
                        </div>
                        
                        {isLoading && <div className="loader"></div>}
                        {error && !isLoading && <p className="error-message">{error}</p>}
                        
                        <div className="results-grid">
                            {documents.map((doc, index) => (
                                <div key={index} className="result-item">
                                    <img
                                        src={`data:image/jpeg;base64,${doc.data}`}
                                        alt={doc.filename}
                                    />
                                    <span>{doc.filename}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;