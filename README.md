# 🕵️ AI-Powered E-commerce QA Demo

An intelligent quality assurance system that uses AI agents to automatically test e-commerce websites, powered by [Kernel](https://onkernel.com) and [Browser Use](https://github.com/gregpr07/browser-use).

## 🎯 What This Does

This demo showcases automated QA testing of e-commerce websites using AI agents that can:

- **Product Page Assessment**: Navigate to product pages, evaluate if product images match descriptions, and add items to cart
- **Cart Page Validation**: Check cart pages for specific promotional banners and offers
- **Generate Review Links**: Create browser replay recordings of all agent actions for detailed review

Each test phase is recorded as a separate browser replay, allowing you to see exactly what the AI agents did and how they reached their conclusions.

## 🚨 Important Prerequisites & Limitations

**⚠️ This is a demonstration template, not a plug-and-play solution.** To reproduce this functionality, you'll need:

### Required Infrastructure
- **Kernel Platform Access**: Active Kernel account with API access ([docs.onkernel.com](https://docs.onkernel.com))
- **Anthropic API Key**: For Claude AI agent functionality ([console.anthropic.com](https://console.anthropic.com))
- **Development Shopify Store**: A test store with password protection enabled
- **Store Password**: Access credentials for your development store

### Customization Requirements
- **Agent Tasks Must Be Customized**: The current tasks are specific to our test store and promotion types
- **Product URLs**: You'll need to update product URLs to match your test store
- **Expected Behaviors**: Modify the agent instructions based on what you want to test
- **Assessment Criteria**: Adapt the pass/fail criteria to your specific QA requirements

**This demo is designed to show the approach and framework - you will need to customize the agent tasks, URLs, and validation logic for your specific use case.**

## 📋 Prerequisites

Before you can run this demo, ensure you have:

1. **Python 3.11+** installed
2. **Kernel CLI** installed and configured ([installation guide](https://docs.onkernel.com/cli/install))
3. **Anthropic API key** with Claude access
4. **Development Shopify store** (or similar e-commerce platform)
5. **UV package manager** (recommended) or pip

## 🚀 Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <this-repository>
cd replays-demo
uv install  # or pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# For running the demo client
KERNEL_API_KEY=your_kernel_api_key_here

# For deployment (can also be set via -e flag)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
STORE_PASSWORD=your_shopify_store_password
```

### 3. Customize for Your Store

**⚠️ Critical Step**: Update the following in `main.py` and `demo-qa-agent.py`:

- Replace `kernel-test-store-1.myshopify.com` with your store URL
- Modify product URLs in the demo script
- Customize agent task instructions for your specific QA scenarios
- Update expected promotional text and validation criteria

### 4. Deploy to Kernel

```bash
kernel deploy main.py --env-file .env
```

### 5. Run the Demo

```bash
uv run demo-qa-agent.py
```

## 🏗️ Architecture Overview

### Core Components

- **main.py**: Kernel app with the `storefront-qa-agent` action
- **session.py**: Custom browser session handling for CDP connections
- **demo-qa-agent.py**: Client script that invokes the Kernel app and displays results

### How It Works

1. **Invocation**: Demo script calls the Kernel app via API
2. **Browser Creation**: Kernel provisions a managed browser session
3. **Phase 1**: AI agent navigates to product page, assesses image/title match, adds to cart
4. **Phase 2**: AI agent navigates to cart, checks for promotional banners
5. **Replay Generation**: Each phase creates a reviewable browser recording
6. **Results**: Structured assessment data and replay links returned

### AI Agent Flow

```
Product URL → AI Agent 1 → Product Assessment + Cart Addition
     ↓
Cart Page → AI Agent 2 → Promotional Banner Assessment
     ↓
Structured Results + Replay Links
```

## 🛠️ Customization Guide

### Adapting Agent Tasks

The current agents are configured for specific scenarios. To customize:

1. **Update Product Assessment** (main.py:72-84):
   - Modify the product evaluation criteria
   - Change expected product types or attributes
   - Adjust cart addition logic

2. **Update Cart Assessment** (main.py:112-124):
   - Replace promotional text with your offers
   - Modify banner detection logic
   - Add additional cart validation steps

3. **Add New Assessment Phases**:
   - Create additional agent instances
   - Add new replay recording phases
   - Update the QAResult structure

## 📺 Demo Walkthrough

When you run `uv run demo-qa-agent.py`, you'll see:

1. **Invocation Start**: API call to Kernel platform
2. **Progress Updates**: Real-time polling of execution status  
3. **Results Display**: Formatted assessment verdicts
4. **Replay Links**: Clickable URLs to review agent actions

## ⚠️ Limitations & Considerations

### Customization Needs
- **Store-Specific Logic**: Must adapt agent tasks to your store's layout and flow
- **Product Catalog**: Update product URLs and expected content
- **Validation Criteria**: Modify pass/fail logic for your QA requirements
- **Authentication**: May need to handle different login/access patterns

## 🔧 Troubleshooting

### Common Issues

**"Store password incorrect"**  
- Ensure STORE_PASSWORD matches your Shopify development store password
- Verify the store URL is accessible and password-protected

**"Agent task failed"**
- Check that product URLs are valid and accessible
- Verify your store layout matches the expected agent navigation flow
- Review browser replay links to see where agents encountered issues

**"Deployment failed"**
- Ensure all required environment variables are set
- Check that your Kernel CLI is properly authenticated via `kernel login`

### Getting Help

- **Kernel Documentation**: [docs.onkernel.com](https://docs.onkernel.com)
- **Browser Use SDK**: [https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use)
- **Anthropic API**: [docs.anthropic.com](https://docs.anthropic.com)