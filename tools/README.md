# Development Tools

This directory contains scripts and tools used for internal development and maintenance of the OpenAPI specifications. These are primarily for maintainers and contributors rather than end users.

## Tools Overview

### `split_endpoint.py`

This script processes vendor OpenAPI specifications (from `vendor/openapi/`) and converts them into our modular structure in the `openapi/` directory. It:

1. Splits monolithic OpenAPI specs into modular components
2. Organizes endpoints, parameters, responses, and schemas into separate files
3. Creates relative references between components

**Usage:** This script is typically run during the initial setup or when updating specifications from vendor sources. End users generally don't need to run this directly.

### Generation Scripts

#### For Windows

- `generate_binance_python_client.bat` - Generates a Python client for Binance API

#### For macOS/Linux

- `generate_binance_python_client.sh` - Generates a Python client for Binance API

These scripts use OpenAPI Generator to create client code from our specifications. They are primarily used during development to test that the specifications remain valid and can generate working client code.

## Note for Contributors

When adding new tools to this directory, please:

1. Document their purpose and usage in this README
2. Ensure they work across different platforms where possible
3. Include appropriate error handling and logging 