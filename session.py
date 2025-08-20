from browser_use import BrowserSession

# Define a subclass of BrowserSession that overrides _setup_viewports (which mishandles resizing on connecting via cdp)
class BrowserSessionCustomResize(BrowserSession):
    async def _setup_viewports(self) -> None:
        """Resize any existing page viewports to match the configured size, set up storage_state, permissions, geolocation, etc."""

        assert self.browser_context, 'BrowserSession.browser_context must already be set up before calling _setup_viewports()'

        self.browser_profile.window_size = {"width": 1024, "height": 786}
        self.browser_profile.viewport = {"width": 1024, "height": 786}
        self.browser_profile.screen = {"width": 1024, "height": 786}
        self.browser_profile.device_scale_factor = 1.0

        # log the viewport settings to terminal
        viewport = self.browser_profile.viewport
        
        # if we have any viewport settings in the profile, make sure to apply them to the entire browser_context as defaults
        if self.browser_profile.permissions:
            try:
                await self.browser_context.grant_permissions(self.browser_profile.permissions)
            except Exception as e:
                print(e)
                
        try:
            if self.browser_profile.default_timeout:
                self.browser_context.set_default_timeout(self.browser_profile.default_timeout)
            if self.browser_profile.default_navigation_timeout:
                self.browser_context.set_default_navigation_timeout(self.browser_profile.default_navigation_timeout)
        except Exception as e:
            print(e)
            
        try:
            if self.browser_profile.extra_http_headers:
                self.browser_context.set_extra_http_headers(self.browser_profile.extra_http_headers)
        except Exception as e:
            print(e)

        try:
            if self.browser_profile.geolocation:
                await self.browser_context.set_geolocation(self.browser_profile.geolocation)
        except Exception as e:
            print(e)

        await self.load_storage_state()

        page = None

        for page in self.browser_context.pages:
            if viewport:
                await page.set_viewport_size(viewport)

            if page.url == 'about:blank':
                # Add a DVD screensaver-style loading animation for blank pages
                await page.evaluate("""
                    document.body.innerHTML = `
                        <div style="
                            position: fixed;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            font-family: Arial, sans-serif;
                            font-size: 24px;
                            color: #666;
                            animation: bounce 2s infinite alternate;
                        ">
                            Loading...
                        </div>
                        <style>
                            @keyframes bounce {
                                0% { transform: translate(-50%, -50%) scale(1); }
                                100% { transform: translate(-50%, -50%) scale(1.1); }
                            }
                        </style>
                    `;
                """)

        # Try to resize browser windows using CDP
        if self.browser_profile.window_size:
            try:
                # Attempt to resize the window
                window_size = self.browser_profile.window_size
                if page:
                    await page.evaluate(f"window.resizeTo({window_size['width']}, {window_size['height']})")
            except Exception as e:
                print(f"Failed to resize window: {e}")
                # Fallback to JavaScript window resizing if CDP method fails
                if page:
                    try:
                        await page.evaluate(f"""
                            window.moveTo(0, 0);
                            window.resizeTo({window_size['width']}, {window_size['height']});
                        """)
                    except Exception as fallback_error:
                        print(f"Fallback resize also failed: {fallback_error}")