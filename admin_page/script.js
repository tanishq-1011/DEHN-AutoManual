// script.js (UPDATED VERSION)
'use strict';

document.addEventListener('DOMContentLoaded', () => {

    const fileInput = document.getElementById('file-input');
    const feedbackMessage = document.getElementById('feedback-message');

    fileInput.addEventListener('change', (event) => {
        const files = event.target.files;
        if (files.length > 0) {
            const selectedFile = files[0];
            feedbackMessage.textContent = `File selected: "${selectedFile.name}"`;
            feedbackMessage.classList.remove('success');
            handleFileUpload(selectedFile);
        }
    });

    /**
     * Handles the file upload process.
     * This now calls our local Python/FastAPI backend.
     * @param {File} file The file object selected by the user.
     */
    function handleFileUpload(file) {
        feedbackMessage.textContent = 'Uploading...';

        // Create a FormData object to send the file
        const formData = new FormData();
        // The key 'manualFile' MUST match the parameter name in our Python function
        formData.append('manualFile', file);

        // Use fetch to send the file to your Python backend
        fetch('http://127.0.0.1:8000/uploadfile/', { // The URL of your FastAPI server
            method: 'POST',
            body: formData
        })
        .then(response => {
            // Check if the response is successful
            if (!response.ok) {
                // If not, create an error to be caught by the .catch block
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            // If successful, parse the JSON response from the server
            return response.json();
        })
        .then(data => {
            console.log('Success response from server:', data);
            // Display a success message using the data returned from the server
            feedbackMessage.textContent = `Success! "${data.filename}" uploaded.`;
            feedbackMessage.classList.add('success');
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            feedbackMessage.textContent = 'Upload failed. Is the backend server running?';
            feedbackMessage.classList.remove('success');
        });
    }
});