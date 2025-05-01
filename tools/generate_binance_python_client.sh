#!/bin/bash

# --- Get script directory ---
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# --- Settings ---
INPUT_SPEC="$ROOT_DIR/openapi/binance/openapi.yaml"
OUTPUT_DIR="$ROOT_DIR/generated/binance_python_client"

echo "[INFO] Current directory: $(pwd)"
echo "[INFO] Script directory: $SCRIPT_DIR"
echo "[INFO] Root directory: $ROOT_DIR"
echo "[INFO] OpenAPI specification file: $INPUT_SPEC"
echo "[INFO] Output directory: $OUTPUT_DIR"

# --- Check if Java is available ---
if ! command -v java &> /dev/null; then
    echo "[ERROR] Java not found. Please install Java and add it to PATH."
    exit 1
fi

# --- Check if openapi-generator-cli is available ---
if ! command -v openapi-generator-cli &> /dev/null; then
    echo "[ERROR] openapi-generator-cli not found."
    echo "[TIP] Please install first: npm install @openapitools/openapi-generator-cli -g"
    exit 1
fi

# --- First run the split script ---
echo "[INFO] Running split script to generate modular OpenAPI specification files..."
python "$SCRIPT_DIR/split_endpoint.py"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to split OpenAPI specification files."
    exit 1
fi

# --- Check if OpenAPI specification file exists ---
if [ ! -f "$INPUT_SPEC" ]; then
    echo "[ERROR] OpenAPI specification file not found: $INPUT_SPEC"
    exit 1
fi

# --- Clean up old output directory (if exists) ---
if [ -d "$OUTPUT_DIR" ]; then
    echo "[INFO] Cleaning up old output directory: $OUTPUT_DIR"
    rm -rf "$OUTPUT_DIR"
fi

# --- Generate Python client ---
echo "[INFO] Using $INPUT_SPEC to generate Binance Python client to $OUTPUT_DIR ..."

mkdir -p "$OUTPUT_DIR"

echo "[INFO] Using openapi-generator-cli to generate code..."
openapi-generator-cli generate -i $INPUT_SPEC -g python -o $OUTPUT_DIR --skip-validate-spec --additional-properties=packageName=binance_client,useTags=true,enumPropertyNaming=UPPERCASE

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to generate Binance Python client."
    exit 1
fi

echo
echo "[SUCCESS] Binance Python client has been successfully generated at: $OUTPUT_DIR"
echo "[TIP] You can navigate to $OUTPUT_DIR and follow the instructions to install and use." 