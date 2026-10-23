# CONN-ARR-MCP-SDK-CENTRALIZATION — Capabilities through the SDK

Owner: .. Cross-repo IDs: `SDK-CENTRALIZED-CAPABILITIES-R001`, `SDK-CENTRALIZED-CAPABILITIES-R003`, `SDK-CENTRALIZED-CAPABILITIES-R008`, `SDK-CENTRALIZED-CAPABILITIES-R040`.

Extends: [SDK-CENTRALIZED-CAPABILITIES](https://github.com/Knuckles-Team/agent-connector-sdk/blob/main/specs/centralized-capabilities/spec.md)

## Purpose and user stories

The connector must reach the arr media services through the SDK. The SDK owns the governed HTTP client, retry, TLS profiles and optional dependencies.

An operator points the connector at the arr media services. Transport security and retries come from the SDK, not from connector code.

## Requirements and acceptance

The rows are in [requirements.md](requirements.md). The proving tests are in [test-spec.md](test-spec.md).

## Why a new spec

The search covered `specs/` of this repository and the SDK centralized-capabilities spec. This repository had no spec for these capabilities. The SDK owns them. This spec states how this connector uses them.

## Scope and interfaces

In scope: the connector's HTTP client, retry handling, TLS handling and dependency pins.

Out of scope: the tool surface, which stays one tool per API operation, and the SDK modules themselves.
