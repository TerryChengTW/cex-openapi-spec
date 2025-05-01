# OpenAPI AI & Codegen Guidelines

This document defines the canonical conventions and rules for all OpenAPI schemas in this repository. **All code generation, AI tools, and human contributors must follow these guidelines.**

## 📁 File Structure

- OpenAPI specifications are organized by functional types:
  - `parameters/`: Contains API request parameter definitions
  - `paths/`: Contains API endpoints organized by service type (e.g., `spot/`)
  - `responses/`: Contains API response definitions
  - `schemas/`: Contains data model definitions
- Development tools and scripts are located in the `tools/` directory

## 📝 Naming Conventions

**Endpoint File Naming:**
- Use the endpoint's functional name for file naming (e.g., `ping.yaml`, `time.yaml`, `depth.yaml`).

**Schema/Type Naming:**
- Use **PascalCase** (each word capitalized, no underscores) for all schema/type names. Example: `ExchangeInfoResponse`, `OrderBookItem`, `ServerTimeResponse`.

**Property/Parameter Naming:**
- Use **camelCase** (first word lowercase, subsequent words capitalized, no underscores) for all object properties, parameters, and response fields, regardless of the exchange. Example: `orderId`, `serverTime`, `symbol`.

## ✅ Best Practices

- Always use `$ref` with relative paths to reference external schemas for responses, parameters, and models. Example: `$ref: '../responses/ping_get_200.yaml'`.
- Provide `example` for both request parameters and response bodies.
- Remove deprecated or renamed schema files promptly to avoid confusion.
- Never invent or hallucinate request/response examples or fields. If an example is not available, leave it blank or request clarification.

## 🏷️ Tags and Documentation

- Ensure all tags in OpenAPI files have clear, concise English descriptions.
- Keep this file updated with any new conventions, naming rules, or architectural decisions.
- All documentation and comments must be in English.

## ⚙️ Code Generation

- Development scripts for code generation are available in the `tools/` directory for both Windows and macOS/Linux platforms
- The generation process uses the OpenAPI Generator CLI to create Python clients from the OpenAPI specifications.
- **IMPORTANT**: Most exchange authentication processes cannot be fully described by OpenAPI specifications as they involve dynamic signature generation based on timestamps and other algorithms.
- **NOTE**: The generated code will require manual modifications, especially for authentication flows, before it can be used in production.
- This project's primary purpose is to provide machine-readable specifications that allow AI to understand the latest exchange API structures.

## 🔄 Updates and Maintenance

- When renaming or deleting schema files, update all `$ref` references accordingly to prevent broken links.
- If naming conventions change (e.g., camelCase to snake_case), document the migration steps and update all files consistently.

---

**All contributors and AI tools must read and follow this document before making any changes or generating code.**
