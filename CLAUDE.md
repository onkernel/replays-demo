# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Kernel application that demonstrates automated QA testing for e-commerce websites using Browser Use SDK and AI agents. The application performs quality assurance checks on a Shopify test store, evaluating product page accuracy and cart promotional banners, then generates browser replay links for review.

## Key Components

- **main.py**: Core Kernel app with `storefront-qa-agent` action that orchestrates the two-phase QA testing workflow
- **session.py**: Custom browser session class (`BrowserSessionCustomResize`) that provides proper viewport handling and window resizing when connecting via CDP
- **demo-qa-agent.py**: Standalone demo script that invokes the Kernel app via API and displays formatted results
- **pyproject.toml**: Project configuration with dependencies for browser-use, kernel, anthropic, and supporting libraries

## Architecture

The application implements a dual-agent QA approach:

### Phase 1: Product Page Assessment
- AI agent navigates to the specified product URL
- Examines product image vs title description for accuracy
- Adds item to cart
- Returns PASS/FAIL verdict with assessment text

### Phase 2: Cart Page Assessment  
- AI agent navigates to cart page via UI
- Searches for promotional banners
- Specifically validates "$20 off when you spend $100" promotion display
- Returns PASS/FAIL verdict with assessment text

Each phase records a separate browser replay for detailed review.

## Dependencies

- **browser-use** (~0.5.3): Browser automation framework with AI agent capabilities
- **kernel** (>=0.8.1): Kernel platform SDK for deployment and browser management
- **anthropic** (>=0.40.0): Claude AI integration for intelligent agents
- **pydantic** (>=2.10.6): Data validation and structured return types
- **requests** (>=2.25.1): HTTP client for API calls
- **python-dotenv** (>=0.19.0): Environment variable management

## Environment Variables

Required environment variables:
- **ANTHROPIC_API_KEY**: Claude API key for AI agent functionality
- **STORE_PASSWORD**: Password for accessing the test Shopify store
- **KERNEL_API_KEY**: Required for demo script API invocations

## Deployment

Deploy the Kernel app:
```bash
kernel deploy main.py --env-file .env
```

Run the demo client:
```bash
uv run demo-qa-agent.py
```

## Technical Implementation Details

### AI Model Configuration
- Uses Claude Sonnet 4 (`claude-sonnet-4-20250514`) for intelligent browser automation
- Agents receive structured task instructions with specific output format requirements
- Plain text responses enforced (no markdown formatting)

### Browser Session Management
- Fixed 1024x786 viewport configuration across all browser contexts
- Custom `BrowserSessionCustomResize` class handles CDP connection viewport issues
- Includes fallback window resizing mechanisms and loading animations for blank pages
- Proper browser session cleanup in finally blocks

### Kernel Replays Integration
- Sequential replay recording: product phase → cart phase
- Replay view URLs provided in structured response for user review

### Security Features
- Sensitive data handling via `sensitive_data` dictionary for store passwords
- Environment variable isolation during deployment
- No hardcoded credentials in source code

### Error Handling
- Comprehensive try/catch blocks around replay operations
- Graceful degradation when agent tasks fail
- Structured error messaging in assessment results
- Guaranteed browser session cleanup

## Data Structures

### TaskInput
```python
class TaskInput(TypedDict):
    product_url: str
```

### QAResult
```python
class QAResult(TypedDict):
    product_page_replay_link: str
    cart_page_replay_link: str
    product_image_assessment: str
    cart_banner_assessment: str
```

## Demo Application Features

The `demo-qa-agent.py` provides:
- Async Kernel app invocation with polling
- Formatted console output with colored verdicts
- Structured result display with replay links
- Execution timing and error handling
- User-friendly troubleshooting guidance

## QA Agent Design Patterns

For effective QA automation:
- Separate browser replays for distinct testing phases
- Structured agent task descriptions with explicit output format requirements
- Comprehensive error handling for both browser and agent failures
- TypedDict return structures for API consistency
- Secure credential handling via environment variables and sensitive_data patterns