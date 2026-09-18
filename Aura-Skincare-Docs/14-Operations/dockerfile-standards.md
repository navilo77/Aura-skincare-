14-Operations/docker/dockerfile-standards.md
````markdown
# Dockerfile Standards

---

Document ID: OPS-023

Title: Dockerfile Standards

Version: 1.0.0

Status: Approved

Owner: Aura Skincare

Category: Operations

Last Updated: 2026-09-16

---

# Purpose

Defines the enterprise standards for creating, maintaining, and securing Dockerfiles used across the Aura platform.

---

# Objectives

- Standardize Docker image creation.
- Improve build consistency.
- Reduce image size.
- Improve security.
- Enable reproducible builds.
- Support CI/CD automation.

---

# Scope

These standards apply to all containerized services, including:

- Backend API
- Frontend
- AI Services
- AI Gateway
- Worker Services
- n8n Custom Images
- Utility Services

---

# Base Image Policy

Approved base images should:

- Be official or organization-approved.
- Be actively maintained.
- Use minimal distributions where practical.
- Be pinned to a specific version.

Preferred examples:

- node:22-alpine
- python:3.12-slim
- nginx:stable-alpine

Avoid:

- latest
- Untrusted images
- End-of-life distributions

---

# Layer Optimization

Dockerfiles should:

- Combine related RUN commands.
- Remove temporary files.
- Minimize the number of layers.
- Copy only required files.

Example workflow:

1. Copy dependency files.
2. Install dependencies.
3. Copy application source.
4. Build application.
5. Clean temporary artifacts.

---

# Multi-Stage Builds

Use multi-stage builds for production images.

Benefits:

- Smaller image size
- Improved security
- Faster deployment
- Reduced attack surface

Typical stages:

Build

↓

Test (optional)

↓

Production

---

# User Permissions

Containers should:

- Run as a non-root user.
- Use the least privilege principle.
- Restrict filesystem access where possible.

Avoid:

USER root

unless explicitly justified.

---

# Environment Variables

Configuration should come from:

- .env
- Environment Variables
- Docker Secrets
- Secret Manager

Never store:

- API Keys
- Passwords
- JWT Secrets
- Database Credentials

inside Dockerfiles.

---

# File Management

Use a `.dockerignore` file.

Exclude:

- node_modules
- .git
- logs
- temporary files
- local configuration
- test artifacts

---

# Security Requirements

Dockerfiles should:

- Pin dependency versions.
- Scan images for vulnerabilities.
- Remove build tools from runtime images.
- Minimize installed packages.
- Avoid unnecessary Linux capabilities.

---

# Image Metadata

Recommended OCI labels:

- Title
- Description
- Version
- Vendor
- Source Repository
- License

Example:

org.opencontainers.image.title

org.opencontainers.image.version

---

# Health Check

Production containers should define a HEALTHCHECK where applicable.

Examples:

- API
- AI Gateway
- Worker
- Web Server

---

# Build Standards

Builds must be:

- Repeatable
- Deterministic
- Automated
- CI/CD Compatible

Images should be versioned using:

- Semantic Version
- Git Commit SHA
- Build Number

---

# Validation Checklist

Before publishing an image:

- Base image approved
- Multi-stage build used
- Non-root user configured
- Secrets excluded
- Image scanned
- HEALTHCHECK defined
- .dockerignore configured
- Build successful

---

# Related Documents

- docker-compose.md
- image-versioning.md
- container-security.md
- deployment-strategy.md
- secrets-management.md

---

# Core Principle

Every Dockerfile must produce secure, minimal, reproducible, and production-ready container images that follow enterprise operational and security standards.