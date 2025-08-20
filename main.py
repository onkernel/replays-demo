from browser_use.llm import ChatAnthropic
from browser_use import Agent
import kernel
from kernel import Kernel
from typing import TypedDict
from session import BrowserSessionCustomResize
import os

client = Kernel()

app = kernel.App("kernel-test-store-1-qa")

class TaskInput(TypedDict):
    product_url: str
    
# Environment variables are set during `kernel deploy <filename> -e VAR_NAME=value`
# See https://docs.onkernel.com/launch/deploy#environment-variables
llm = ChatAnthropic(model="claude-sonnet-4-20250514")

STORE_PASSWORD = os.getenv("STORE_PASSWORD")

class QAResult(TypedDict):
    product_page_replay_link: str
    cart_page_replay_link: str
    product_image_assessment: str
    cart_banner_assessment: str

@app.action("storefront-qa-agent")
async def storefront_qa_agent(ctx: kernel.KernelContext, input_data: TaskInput) -> QAResult:
    """
    🕵️ AI-powered e-commerce QA detective/agent that catches sneaky product mismatches and offers! 
    
    This function deploys two specialized AI agents to hunt down quality issues:
    • 🎯 Product Detective: Checks if product images actually match their titles.
    • 🎁 Promotion Hunter: Verifies cart banners display the correct Offer deal.
    
    Each agent records its investigation as a browser replay for your viewing pleasure.
    
    Args:
        ctx: Kernel context containing invocation information
        input_data: An object with product_url to investigate
        
    Returns:
        QAResult with replay links and hilarious AI verdicts on what they found
    """
    
    kernel_browser = client.browsers.create(invocation_id=ctx.invocation_id)
    print("Kernel browser live view url: ", kernel_browser.browser_live_view_url)
    
    browser_session = BrowserSessionCustomResize(cdp_url=kernel_browser.cdp_ws_url)
    
    # Initialize results
    product_page_replay_link = ""
    cart_page_replay_link = ""
    product_image_assessment = ""
    cart_banner_assessment = ""
    
    try:
        # Create sensitive data dictionary for secure password handling
        sensitive_data = {
            "https://kernel-test-store-1.myshopify.com": {
                "STORE_PASSWORD": STORE_PASSWORD
            }
        }
        
        # Start first replay for product page
        product_replay = client.browsers.replays.start(kernel_browser.session_id)
        
        # Create agent for product page assessment
        product_agent = Agent(
            task=f"""
            1. Navigate to {input_data['product_url']}. 
            2. Examine the product image and title. 
            3. Check if the product image accurately represents what the product title describes. 
            4. Then add the item to the cart. 
            5. Return your response as a single paragraph of text in this format: 'VERDICT: [PASS/FAIL] - [1-3 sentence assessment]'
            
            IMPORTANT OUTPUT FORMAT:
            - Use ONLY plain text - no markdown, bullets, or special formatting
            - Return EXACTLY one line/paragraph of text
            - Do NOT use **, *, #, -, •, or any other formatting characters
            - Example: "VERDICT: PASS - The product image clearly shows a blue ceramic vase which matches the product title."
            
            The store password is STORE_PASSWORD if you need it.
            """,
            llm=llm,
            browser_session=browser_session,
            sensitive_data=sensitive_data
        )
        
        product_result = await product_agent.run()
        
        # Stop product page replay
        try:
            client.browsers.replays.stop(replay_id=product_replay.replay_id, id=kernel_browser.session_id)
            product_page_replay_link = product_replay.replay_view_url
        except Exception as e:
            print(f"Error stopping product replay: {str(e)}")
            raise
        
        # Extract product assessment from result
        if product_result.final_result():
            product_image_assessment = product_result.final_result()
        else:
            product_image_assessment = "Error: Could not complete product image assessment"
        
        # Start second replay for cart page
        cart_replay = client.browsers.replays.start(kernel_browser.session_id)
        
        # Create agent for cart page assessment
        cart_agent = Agent(
            task=f"""
            1. Navigate to the cart page using the website's UI navigation. 
            2. Once on the cart page, look for any conditional banner or promotional message about coupon offerings. 
            3. Specifically check if there's a banner showing a '$20 off when you spend $100' promotion. 
            4. Return your response as a single paragraph of text in this format: 'VERDICT: [PASS/FAIL] - [1-3 sentence assessment]'
            
            IMPORTANT OUTPUT FORMAT:
            - Use ONLY plain text - no markdown, bullets, or special formatting
            - Return EXACTLY one line/paragraph of text
            - Do NOT use **, *, #, -, •, or any other formatting characters
            - Example: "VERDICT: FAIL - The cart page shows a '$15 off when you spend $75' banner instead of the expected '$20 off when you spend $100' promotion."
            
            The store password is STORE_PASSWORD if you need it.
            """,
            llm=llm,
            browser_session=browser_session,
            sensitive_data=sensitive_data
        )
        
        cart_result = await cart_agent.run()
        
        # Stop cart page replay
        try:
            client.browsers.replays.stop(replay_id=cart_replay.replay_id, id=kernel_browser.session_id)
            cart_page_replay_link = cart_replay.replay_view_url
        except Exception as e:
            print(f"Error stopping cart replay: {str(e)}")
            raise
        
        # Extract cart assessment from result
        if cart_result.final_result():
            cart_banner_assessment = cart_result.final_result()
        else:
            cart_banner_assessment = "Error: Could not complete cart banner assessment"
                
    except Exception as e:
        print(f"Error during QA flow: {str(e)}")
        if not product_image_assessment:
            product_image_assessment = f"Error: {str(e)}"
        if not cart_banner_assessment:
            cart_banner_assessment = f"Error: {str(e)}"
    
    finally:
        # Ensure browser session is closed
        try:
            await browser_session.close()
        except:
            pass
    
    # Return structured result
    return QAResult(
        product_page_replay_link=product_page_replay_link,
        cart_page_replay_link=cart_page_replay_link,
        product_image_assessment=product_image_assessment,
        cart_banner_assessment=cart_banner_assessment
    )