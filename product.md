# Product: Simple URL Shortener

## Overview
A lightweight URL shortening service that converts long, unwieldy URLs into compact, shareable short links. When someone visits a short link, the service instantly redirects them to the original long URL.

## Problem Statement
Long URLs are hard to share, type, and remember — especially across messaging apps, printed media, and character-limited platforms. Existing commercial shorteners (bit.ly, tinyurl) come with analytics, ads, and third-party dependency. This project provides a minimal, self-hostable alternative.

## Target Users
- Developers who want to self-host their own shortener
- Individuals who want a private, no-tracking URL shortener
- Anyone learning backend development (Flask + SQLite)

## Core Features
- Accept a long URL and return a unique short code
- Store the long-URL ↔ short-code mapping in a database
- Redirect visitors from a short URL to the original long URL
- Basic web frontend to paste a URL and copy the shortened result

## User Stories
- As a user, I want to paste a long URL and get back a short link so I can share it easily.
- As a user, I want to visit the short link and be taken to the original URL so it works like any normal link.
- As a user, I want the short code to be unique each time so I never get someone else's link.

## Non-Goals (out of scope for v1)
- User accounts / authentication
- Click analytics or tracking
- Custom vanity slugs
- Link expiration or deletion
- Rate limiting and anti-abuse

## Tech Stack
- Backend: Python + Flask
- Database: SQLite (via Python's built-in `sqlite3`)
- Frontend: Minimal HTML/CSS/JS served by Flask

## Success Criteria
- Shortening a URL returns a unique short code
- Visiting the short URL redirects (HTTP 302) to the original URL
- Links persist across server restarts (SQLite file storage)
- Frontend shows the shortened link with a copy button
