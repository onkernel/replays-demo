# 🕵️ AI-Powered E-commerce QA Demo

> **Watch AI agents autonomously test your e-commerce site and generate reviewable browser replays**

An intelligent quality assurance system that uses AI agents to automatically test e-commerce websites, powered by [Kernel](https://onkernel.com) and [Browser Use](https://github.com/browser-use/browser-use).

[![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)](https://kernel.onkernel.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Kernel Replays Youtube Video Screenshot](https://github.com/user-attachments/assets/369bfca3-9f52-425a-b754-dab8d7e47f33)](https://www.youtube.com/watch?v=eFXD75U60Bc)

---

## 💡 Why This Matters

Traditional QA testing is manual, time-consuming, and error-prone. This demo shows how AI agents can:

- ✅ **Automate visual testing** - Agents "see" and evaluate product images like a human QA tester would
- 🔄 **Execute complex workflows** - Navigate multi-step user journeys autonomously
- 📹 **Provide reviewable evidence** - Every action is recorded as a browser replay
- 🎯 **Scale effortlessly** - Test hundreds of products in the time it takes to test one manually

This is the future of QA: AI agents that think, see, and validate like your best QA engineer.

## 🎯 What This Demo Does

This application showcases **dual-phase AI-powered QA testing** on e-commerce sites:

### Phase 1: Product Page Intelligence 🛍️
- **Navigate** to product URLs autonomously
- **Evaluate** if product images accurately match title descriptions
- **Interact** with the page to add items to cart
- **Report** PASS/FAIL verdict with detailed assessment

### Phase 2: Cart Page Validation 🛒
- **Navigate** to cart using the site's natural UI flow
- **Search** for promotional banners and special offers
- **Validate** specific promotion text (e.g., "$20 off when you spend $100")
- **Report** PASS/FAIL verdict with findings

### Phase 3: Replay Generation 🎥
Each testing phase is automatically recorded as a **browser replay**, allowing you to:
- See exactly what the AI agent saw
- Review the agent's decision-making process
- Debug failures by watching agent interactions
- Share results with your team

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Autonomous AI Agents** | Claude-powered agents that understand context and make intelligent decisions |
| 🎬 **Browser Replays** | Every test generates a reviewable recording via Kernel's replay system |
| 🔍 **Visual Understanding** | AI agents can "see" and evaluate images, layouts, and visual elements |
| 📊 **Structured Results** | Clean PASS/FAIL verdicts with detailed assessment narratives |
| 🔐 **Secure Credentials** | Built-in sensitive data handling for store passwords and API keys |
| ⚡ **Async Execution** | Non-blocking API calls with polling for efficient testing workflows |
| 🎯 **Multi-Phase Testing** | Sequential test phases with independent replay recordings |

## 🚨 Important: This is a Template

**⚠️ This is a demonstration template, not a plug-and-play solution.**

This repository showcases the **approach and architecture** for building AI-powered QA systems. To adapt it for your use case, you'll need to:

### What You'll Need to Provide
- ✅ **Kernel Platform Access** - Active account with API access ([sign up](https://onkernel.com))
- ✅ **Anthropic API Key** - For Claude AI functionality ([get key](https://console.anthropic.com))
- ✅ **Your Test Environment** - E-commerce site or web application to test
- ✅ **Custom Agent Tasks** - Modify the AI instructions for your specific QA scenarios

### What You'll Need to Customize
- 🔧 **Agent Task Instructions** - Current tasks are specific to our demo store
- 🔧 **Product URLs** - Update to match your test environment
- 🔧 **Validation Logic** - Adapt pass/fail criteria to your requirements
- 🔧 **Expected Behaviors** - Modify based on what you're testing

**Think of this as a blueprint, not a finished product.** The value is in seeing how AI agents, browser automation, and replay recording work together to create autonomous QA workflows.

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

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Demo Client Script                         │
│                    (demo-qa-agent.py)                           │
│                                                                 │
│  • Invokes Kernel app via API                                   │
│  • Polls for completion                                         │
│  • Displays formatted results                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ API Call
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Kernel Platform                             │
│                   (Managed Browser)                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Kernel App (main.py)                        │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Phase 1: Product Page QA                          │  │   │
│  │  │  • Start replay recording                          │  │   │
│  │  │  • AI Agent navigates to product URL               │  │   │
│  │  │  • Evaluate image vs. title match                  │  │   │
│  │  │  • Add item to cart                                │  │   │
│  │  │  • Stop replay → Generate replay link              │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │                         ↓                                │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Phase 2: Cart Page QA                             │  │   │
│  │  │  • Start new replay recording                      │  │   │
│  │  │  • AI Agent navigates to cart                      │  │   │
│  │  │  • Search for promotional banners                  │  │   │
│  │  │  • Validate specific promotion text                │  │   │
│  │  │  • Stop replay → Generate replay link              │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │                         ↓                                │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Return Results                                    │  │   │
│  │  │  • Product assessment + replay link                │  │   │
│  │  │  • Cart assessment + replay link                   │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Purpose | Key Technology |
|-----------|---------|----------------|
| [main.py](main.py) | Kernel app orchestrating the dual-agent QA workflow | Browser Use SDK, Claude Sonnet 4 |
| [session.py](session.py) | Custom browser session with viewport handling for CDP connections | Browser Use + Playwright |
| [demo-qa-agent.py](demo-qa-agent.py) | Client script that invokes the app and displays results | Kernel API, async polling |

### Technology Stack

- **AI Engine**: Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- **Browser Automation**: [Browser Use SDK](https://github.com/browser-use/browser-use) (~0.5.3)
- **Orchestration**: [Kernel Platform](https://onkernel.com) (>=0.8.1)
- **Browser Control**: Playwright (via Browser Use)
- **Language**: Python 3.11+

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

## 📺 Example Output

When you run `uv run demo-qa-agent.py`, you'll see formatted results like this:

```
============================================================
🕵️ E-commerce QA Agent Demo
============================================================

🚀 Starting AI-powered quality assurance testing...
📝 Testing URL: https://kernel-test-store-1.myshopify.com/products/short-sleeved-red-t-shirt

⏳ Invoking QA agents... (this may take 2-3 minutes)
⏳ Invocation started (ID: inv_abc123)... polling for completion

============================================================
📊 QA Results
============================================================
⏱️  Completed in 127.3 seconds
🕐 Timestamp: 2025-09-30 14:23:45

📋 Product Page Assessment
----------------------------------------
✅ VERDICT: PASS - The product image clearly shows a red short-sleeved
t-shirt which accurately matches the product title description. The item
was successfully added to the cart.

📋 Cart Page Assessment
----------------------------------------
❌ VERDICT: FAIL - The cart page displays a '$15 off when you spend $75'
promotional banner instead of the expected '$20 off when you spend $100'
promotion.

📋 Browser Replay Links
----------------------------------------
Review the AI agent's actions by clicking these replay links:

🎬 Product Page Inspection:
   https://replays.onkernel.com/replay/rpl_xyz789

🎬 Cart Page Inspection:
   https://replays.onkernel.com/replay/rpl_abc456

============================================================
✨ Demo Complete! 🎉
============================================================
💡 Key Features Demonstrated:
   • AI agents can autonomously navigate websites
   • Automated quality assurance testing
   • Visual replay links for review and debugging
   • Structured assessment reporting
```

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with:
- [Kernel](https://onkernel.com) - Browser orchestration and replay infrastructure
- [Browser Use](https://github.com/browser-use/browser-use) - AI-powered browser automation
- [Anthropic Claude](https://anthropic.com) - Advanced AI agent intelligence

---

**Ready to build autonomous QA agents?** Start by exploring the code in [main.py](main.py) to see how the dual-phase agent workflow is structured. 🚀
