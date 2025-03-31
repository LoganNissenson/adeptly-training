"""
Script to directly copy static files without using Django's collectstatic
"""

import os
import shutil
from pathlib import Path

# Set the base directory (project root)
BASE_DIR = Path(__file__).resolve().parent

# Define source and destination directories
STATIC_SRC = os.path.join(BASE_DIR, 'static')
STATIC_DEST = os.path.join(BASE_DIR, 'staticfiles')

# Create destination directories if they don't exist
os.makedirs(STATIC_DEST, exist_ok=True)

# Copy all files from static to staticfiles
def copy_directory(src, dest):
    """Copy all files from src to dest directory"""
    print(f"Copying files from {src} to {dest}")
    
    if not os.path.exists(src):
        print(f"Source directory {src} does not exist!")
        return
    
    # Copy all files and directories
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        
        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            copy_directory(s, d)
        else:
            shutil.copy2(s, d)
            print(f"Copied {s} to {d}")

# Perform the copy
if os.path.exists(STATIC_SRC):
    copy_directory(STATIC_SRC, STATIC_DEST)
    print("Static files copied successfully!")
else:
    print(f"Static source directory {STATIC_SRC} does not exist!")
    
    # Create an empty static file to prevent errors
    with open(os.path.join(STATIC_DEST, 'empty.css'), 'w') as f:
        f.write('/* Empty file to prevent static files errors */')
    print("Created empty static file.")
