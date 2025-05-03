#!/bin/bash

# Use OpenAPI Generator to generate a Python API client
# Usage: ./run_api_generator.sh [OpenAPI file path] [output directory] [package name]

# Default parameters
OPENAPI_FILE=${1:-"./openapi/binance/openapi.yaml"}
OUTPUT_DIR=${2:-"./generated/binance_client"}
PACKAGE_NAME=${3:-"binance_client"}

# Helper functions for colored output
function info {
  echo -e "\033[36m$1\033[0m"
}
function success {
  echo -e "\033[32m$1\033[0m"
}
function warn {
  echo -e "\033[33m$1\033[0m"
}
function error {
  echo -e "\033[31m$1\033[0m"
}

# Check if the OpenAPI file exists
if [ ! -f "$OPENAPI_FILE" ]; then
  error "Error: OpenAPI file not found at $OPENAPI_FILE"
  exit 1
fi

# Check if OpenAPI Generator CLI is installed
if ! command -v openapi-generator-cli &> /dev/null; then
  warn "OpenAPI Generator CLI not found. Attempting to install via npm..."
  npm install -g @openapitools/openapi-generator-cli
  if [ $? -ne 0 ]; then
    error "Failed to install OpenAPI Generator CLI. Please install it manually and try again."
    exit 1
  fi
else
  VERSION=$(openapi-generator-cli version)
  success "OpenAPI Generator CLI is installed: $VERSION"
fi

# Ensure output directory exists
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
  warn "Created output directory: $OUTPUT_DIR"
fi

# Run the OpenAPI Generator
info "Starting Python API client generation..."
CMD="openapi-generator-cli generate -i \"$OPENAPI_FILE\" -g python -o \"$OUTPUT_DIR\" --package-name \"$PACKAGE_NAME\" --skip-validate-spec"
info "Running command: $CMD"
eval $CMD

# Check the result
if [ $? -eq 0 ]; then
  success "\nSuccessfully generated Python API client in: $OUTPUT_DIR"
  success "Package name: $PACKAGE_NAME"
  info "\nUsage:"
  echo "cd $OUTPUT_DIR"
  echo "pip install -e ."
  echo "import $PACKAGE_NAME"
else
  error "An error occurred during client generation."
  exit 1
fi
