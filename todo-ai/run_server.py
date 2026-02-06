#!/usr/bin/env python
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set the working directory to the backend folder
os.chdir(backend_dir)

if __name__ == "__main__":
    import uvicorn
    # Run the application with the correct import path
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=7860, reload=True)