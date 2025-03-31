#!/bin/bash

# Create necessary directories
mkdir -p staticfiles
mkdir -p media

# Create an empty CSS file to ensure the static directory is not empty
echo "/* Empty file */" > staticfiles/empty.css

echo "Prestart script completed successfully!"
