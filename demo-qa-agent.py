#!/usr/bin/env python3
"""
🕵️ E-commerce QA Demo - AI-Powered Quality Assurance Testing

This demo showcases automated QA testing of an e-commerce website using AI agents.
The agents will inspect product pages and cart functionality, then generate
replay links for you to review their findings.
"""

import json
import time
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def print_header(title, emoji="🎯"):
    """Print a styled header"""
    print(f"\n{'='*60}")
    print(f"{emoji} {title}")
    print(f"{'='*60}")

def print_section(title, emoji="📋"):
    """Print a styled section header"""
    print(f"\n{emoji} {title}")
    print("-" * 40)

def print_verdict(assessment):
    """Print the verdict with appropriate coloring"""
    if "VERDICT: PASS" in assessment:
        status_emoji = "✅"
        status_color = "\033[92m"  # Green
    elif "VERDICT: FAIL" in assessment:
        status_emoji = "❌"
        status_color = "\033[91m"  # Red
    else:
        status_emoji = "⚠️"
        status_color = "\033[93m"  # Yellow
    
    reset_color = "\033[0m"
    print(f"{status_emoji} {status_color}{assessment}{reset_color}")

def print_replay_link(title, url):
    """Print a replay link in a user-friendly format"""
    print(f"\n🎬 {title}:")
    print(f"   {url}")

def main():
    print_header("E-commerce QA Agent Demo", "🕵️")
    
    print("\n🚀 Starting AI-powered quality assurance testing...")
    print("📝 Testing URL: https://kernel-test-store-1.myshopify.com/products/short-sleeved-red-t-shirt")
    
    app_name = "kernel-test-store-1-qa"
    action_name = "storefront-qa-agent"
    
    start_time = time.time()
    
    print("\n⏳ Invoking QA agents... (this may take 2-3 minutes)")
    
    try:
        # Create async invocation
        response = requests.post(
            "https://api.onkernel.com/invocations",
            headers={
                'Authorization': f"Bearer {os.environ.get('KERNEL_API_KEY')}",
                'Content-Type': 'application/json'
            },
            json={
                "app_name": app_name,
                "action_name": action_name,
                "version": "latest",
                "async": True,
                "payload": json.dumps({"product_url": "https://kernel-test-store-1.myshopify.com/products/short-sleeved-red-t-shirt"})
            }
        )
        
        response.raise_for_status()
        initial_data = response.json()
        invocation_id = initial_data["id"]
        
        print(f"⏳ Invocation started (ID: {invocation_id})... polling for completion")

        # response = client.invocations.follow(invocation_id)
        # print(response)
        
        # Poll for completion
        while True:
            status_response = requests.get(
                f"https://api.onkernel.com/invocations/{invocation_id}",
                headers={'Authorization': f"Bearer {os.environ.get('KERNEL_API_KEY')}"}
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            
            if status_data["status"] == "succeeded":
                result = json.loads(status_data["output"])
                break
            elif status_data["status"] == "failed":
                raise Exception(f"Invocation failed: {status_data.get('status_reason')}")
            
            time.sleep(2)  # Wait 2 seconds before polling again
        
        end_time = time.time()
        duration = round(end_time - start_time, 1)
        
        print_header("QA Results", "📊")
        print(f"⏱️  Completed in {duration} seconds")
        print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Extract results - result already contains the data
        data = result
        
        print_section("Product Page Assessment", "🛍️")
        product_assessment = data.get('product_image_assessment', 'No assessment available')
        print_verdict(product_assessment)
        
        print_section("Cart Page Assessment", "🛒")
        cart_assessment = data.get('cart_banner_assessment', 'No assessment available')
        print_verdict(cart_assessment)
        
        print_section("Browser Replay Links", "🎥")
        print("Review the AI agent's actions by clicking these replay links:")
        
        product_link = data.get('product_page_replay_link', 'Not available')
        cart_link = data.get('cart_page_replay_link', 'Not available')
        
        if product_link != 'Not available':
            print_replay_link("Product Page Inspection", product_link)
        
        if cart_link != 'Not available':
            print_replay_link("Cart Page Inspection", cart_link)
        
        print_header("Demo Complete! 🎉", "✨")
        print("💡 Key Features Demonstrated:")
        print("   • AI agents can autonomously navigate websites")
        print("   • Automated quality assurance testing")
        print("   • Visual replay links for review and debugging")
        print("   • Structured assessment reporting")
        
    except requests.exceptions.HTTPError as e:
        print_header("Error", "❌")
        print(f"Failed to run QA demo: {str(e)}")
        try:
            error_details = e.response.json()
            print(f"Error details: {error_details}")
        except:
            print(f"Response text: {e.response.text}")
        print("\n🔧 Troubleshooting tips:")
        print("   • Ensure your Kernel app is deployed")
        print("   • Check KERNEL_API_KEY environment variable")
        print("   • Verify network connectivity")
    except Exception as e:
        print_header("Error", "❌")
        print(f"Failed to run QA demo: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("   • Ensure your Kernel app is deployed")
        print("   • Check KERNEL_API_KEY environment variable")
        print("   • Verify network connectivity")

if __name__ == "__main__":
    main()