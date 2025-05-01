# Cryptocurrency Exchange OpenAPI Specifications

This repository contains OpenAPI specifications for various cryptocurrency exchanges. The goal is to provide standardized, machine-readable API documentation that can be used to generate client libraries, documentation, and other tools.

## Structure

- `openapi/`: Contains the modular OpenAPI specifications
  - `binance/`: Binance API specifications
  - Other exchanges will be added in the future
- `generated/`: Contains client libraries generated from the OpenAPI specs
- `tools/`: Contains development scripts and utilities (for maintainers)
- `vendor/`: Contains original API specifications from exchanges

## Usage

### For Developers Using These Specs

These specifications can be used directly with OpenAPI tools to:

1. Generate client libraries in various programming languages
2. Create interactive API documentation
3. Test API endpoints
4. Validate API responses

Please refer to the `openapi/GUIDELINES.md` file for detailed information about naming conventions, structure, and best practices.

### For Maintainers

The `tools/` directory contains scripts used for development and maintenance:

- `split_endpoint.py`: Converts vendor specifications into our modular format
- Generation scripts: For testing that specifications can generate working client code

See `tools/README.md` for detailed information about these development tools.

## Notes on Generated Code

**IMPORTANT**: The generated client libraries will require manual modifications before they can be used in production, especially for authentication flows. Most exchange authentication processes involve dynamic signature generation based on timestamps and other algorithms that cannot be fully described in OpenAPI specifications.

This project's primary purpose is to provide accurate, machine-readable specifications that allow developers and AI tools to understand the latest exchange API structures.

## Contributing

Contributions are welcome! Please read `openapi/GUIDELINES.md` before submitting changes to ensure they follow the project's conventions.

## License

This project is licensed under the terms of the MIT license.
