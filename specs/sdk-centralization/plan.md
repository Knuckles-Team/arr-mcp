# CONN-ARR-MCP-SDK-CENTRALIZATION — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Existing system and reuse

The SDK owns the capability rows cited in [requirements.md](requirements.md). The connector adds no transport code of its own.

## Architecture

The connector builds on the SDK. HTTP goes through the SDK governed client, and TLS comes from `resolve_tls_profile` for the connector's settings prefix.

## Interfaces and data model

No tool, argument or result changes.

## Live integration path

Every tool reaches the arr media services through the connector client, which sends each request through the SDK.

## Quality and release gates

The focused tests in [test-spec.md](test-spec.md) must pass. The SDK floor must be the latest published release.

## Risks, alternatives, and decisions

A private certificate authority must be supplied through the TLS profile. A flag that disables verification must not return.
