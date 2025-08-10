# main.py (The Correct, Full Version)

import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI()

# --- CORS Configuration ---
# Allows your frontend to talk to this backend
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500", # Default for VS Code Live Server
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- End CORS Configuration ---


@app.get("/")
def read_root():
    """ A simple endpoint to check if the server is running. """
    return {"status": "DEHN Admin Backend is running"}


# THIS IS THE PART THAT WAS MISSING FROM THE HELLO WORLD VERSION
@app.post("/uploadfile/")
async def create_upload_file(manualFile: UploadFile = File(...)):
    """
    This endpoint receives the file from the frontend.
    It listens on the path "/uploadfile/".
    """
    
    filename = manualFile.filename
    
    # Simulate saving the file and determine its location
    simulated_save_path = os.path.join(os.getcwd(), "uploads", filename)
    
    # Print the info to your backend terminal
    print("--- File Received ---")
    print(f"Filename: {filename}")
    print(f"Simulated Save Location: {simulated_save_path}")
    print("---------------------")
    print("Hello World")
    
    # Return a success message to the frontend
    return {
        "filename": filename,
        "location": simulated_save_path,
        "detail": "File received and 'processed' successfully."
    }