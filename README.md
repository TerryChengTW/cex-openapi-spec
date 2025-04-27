# CEX OpenAPI Spec

> **Note:** This project is an **unofficial** community-driven specification and is not affiliated with or endorsed by any exchange. It aims to provide an accurate, up-to-date, and unified OpenAPI spec for all major CEXs.

A unified, modular, and AI-friendly OpenAPI specification for multiple centralized cryptocurrency exchanges (CEX), designed for seamless aggregation, integration, and cross-exchange tooling.

## Features

- **Unified Structure:** Standardizes endpoints and schemas across all major CEXs (e.g., Binance, OKX, Bybit, KuCoin, etc.).
- **Modular Organization:** Each exchange and endpoint category has its own folder and schema files for easy extension and maintenance.
- **AI & Automation Friendly:** Clear naming, strict example policies, and complete documentation for effortless code generation and AI integration.
- **Extensible:** Easily add new exchanges or endpoints with minimal friction.

## Directory Structure

- `openapi/`
  - `binance/`
  - `okx/`
  - `bybit/`
  - `...`
  - All schemas and endpoints are organized by exchange and functionality.

## Contribution Guidelines

- **Only edit OpenAPI YAML files in `openapi/`.**
- **Use clear, unique, and descriptive names** for all schemas and endpoints.
- **Only use official or real examples** for the `example` field. Never invent or hallucinate data.
- **All documentation must be in English.**
- **Follow folder and naming conventions** as described in `openapi/README.md`.

## Use Cases

- Generate unified SDKs/clients for multiple CEXs.
- Build cross-exchange trading bots and analytics tools.
- Power AI agents with standardized, machine-readable API specs.
