# OpenAPI AI & Codegen Guidelines

This document defines the canonical conventions and rules for all OpenAPI schemas in this repository. **All code generation, AI tools, and human contributors must follow these guidelines.**

## 📁 File Structure

- Endpoints and schemas are organized by exchange and functionality (e.g. `binance/general`, `okx/account`).
- All schema files should be named clearly to indicate their purpose, e.g. `PingResponse.yaml`, `ExchangeInfoResponse.yaml`.

## 📝 Naming Conventions

**Schema/Type Naming:**

- Use **PascalCase** (each word capitalized, no underscores) for all schema/type names and schema file names. Example: `ExchangeInfoResponse`, `OrderBookItem`, `ServerTimeResponse`.

**Property/Parameter Naming:**

- Use **camelCase** (first word lowercase, subsequent words capitalized, no underscores) for all object properties, parameters, and response fields, regardless of the exchange. Example: `orderId`, `serverTime`, `symbol`.

- All schema/model/response files must have unique, descriptive names reflecting their purpose.

## ✅ Best Practices

- Always use `$ref` to reference external schemas for responses and models.
- Provide `example` for both request parameters and response bodies **only if there are official examples**.
- Remove deprecated or renamed schema files promptly to avoid confusion.
- Never invent or hallucinate request/response examples or fields. If an example is not available, leave it blank or request clarification.

## 🏷️ Tags and Documentation

- Ensure all tags in `main.yaml` have clear, concise English descriptions.
- Keep this file updated with any new conventions, naming rules, or architectural decisions.
- All documentation and comments must be in English.

## ⚙️ Code Generation & Example Policy

- Only generate code and OpenAPI schema content that matches the official documentation and real API behavior.
- If you provide a sample input/output (especially response examples), it will be used directly.
- If you do not provide an example, you will be asked if one is available before generating a placeholder or leaving it empty.

## 🔄 Updates and Maintenance

- When renaming or deleting schema files, update all `$ref` references accordingly to prevent broken links.
- If naming conventions change (e.g., camelCase to snake_case), document the migration steps and update all files consistently.

---

**All contributors and AI tools must read and follow this document before making any changes or generating code.**
