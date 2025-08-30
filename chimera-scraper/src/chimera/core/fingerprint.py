import asyncio
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, BrowserContext, Page
from loguru import logger
import random
import json
import os


class AdvancedFingerprintManager:
    """Advanced fingerprint manager with comprehensive anti-detection capabilities."""
    
    def __init__(self):
        self.fingerprint_profiles = self._load_fingerprint_profiles()
        self.current_profile = None
        
    def _load_fingerprint_profiles(self) -> Dict[str, Any]:
        """Load fingerprint profiles from configuration."""
        default_profiles = {
            "desktop_chrome": {
                "viewport": {"width": 1920, "height": 1080},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "platform": "Win32",
                "hardware_concurrency": 8,
                "device_memory": 8,
                "languages": ["en-US", "en"],
                "plugins": [1, 2, 3, 4, 5],
                "timezone": "America/New_York"
            },
            "desktop_firefox": {
                "viewport": {"width": 1920, "height": 1080},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
                "platform": "Win32",
                "hardware_concurrency": 8,
                "device_memory": 8,
                "languages": ["en-US", "en"],
                "plugins": [1, 2, 3, 4, 5],
                "timezone": "America/New_York"
            },
            "mac_chrome": {
                "viewport": {"width": 1440, "height": 900},
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "platform": "MacIntel",
                "hardware_concurrency": 8,
                "device_memory": 8,
                "languages": ["en-US", "en"],
                "plugins": [1, 2, 3, 4, 5],
                "timezone": "America/Los_Angeles"
            }
        }
        
        # Try to load custom profiles from config file
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "fingerprint_profiles.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    custom_profiles = json.load(f)
                    default_profiles.update(custom_profiles)
            except Exception as e:
                logger.warning(f"Failed to load custom fingerprint profiles: {e}")
        
        return default_profiles

    async def create_stealth_browser_context(self, 
                                           proxy: Optional[str] = None, 
                                           profile: str = "desktop_chrome",
                                           browser_type: str = "chromium") -> BrowserContext:
        """Create a stealth browser context with advanced fingerprint spoofing."""
        playwright = await async_playwright().start()
        
        # Select fingerprint profile
        if profile not in self.fingerprint_profiles:
            profile = "desktop_chrome"
        
        self.current_profile = self.fingerprint_profiles[profile]
        
        # Launch browser with anti-detection options
        if browser_type == "chromium":
            browser = await playwright.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--allow-running-insecure-content',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-images'  # Speed up loading
                ]
            )
        else:
            browser = await playwright.firefox.launch(headless=False)
        
        # Set up context options
        context_options = {
            "viewport": self.current_profile["viewport"],
            "user_agent": self.current_profile["user_agent"],
            "locale": self.current_profile["languages"][0],
            "timezone_id": self.current_profile["timezone"]
        }
        
        if proxy:
            context_options["proxy"] = {"server": proxy}
        
        context = await browser.new_context(**context_options)
        
        # Inject advanced stealth scripts
        await self._inject_stealth_scripts(context)
        
        # Set additional properties
        await context.set_extra_http_headers({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        })
        
        return context
    
    async def _inject_stealth_scripts(self, context: BrowserContext):
        """Inject comprehensive stealth scripts to avoid detection."""
        stealth_script = """
        // Override the webdriver property
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Spoof plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Spoof languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
        
        // Spoof Chrome runtime
        window.chrome = {
            runtime: {},
        };
        
        // Spoof hardware concurrency
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => 8,
        });
        
        // Spoof device memory
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 8,
        });
        
        // Spoof platform
        Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32',
        });
        
        // Override permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // Spoof WebGL
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) {
                return 'Intel Inc.';
            }
            if (parameter === 37446) {
                return 'Intel(R) Iris(TM) Graphics 6100';
            }
            return getParameter.apply(this, arguments);
        };
        
        // Spoof canvas fingerprinting
        const originalGetContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function(type, ...args) {
            const context = originalGetContext.apply(this, [type, ...args]);
            if (type === '2d') {
                const originalFillText = context.fillText;
                context.fillText = function(...args) {
                    // Add slight variations to text rendering
                    args[1] += Math.random() * 0.001;
                    args[2] += Math.random() * 0.001;
                    return originalFillText.apply(this, args);
                };
            }
            return context;
        };
        """
        
        await context.add_init_script(stealth_script)
        logger.info(f"Injected stealth scripts for profile: {self.current_profile.get('platform', 'unknown')}")


# Backward compatibility
async def create_stealth_browser_context(proxy: Optional[str] = None, 
                                        user_agent: Optional[str] = None) -> BrowserContext:
    """Legacy function for backward compatibility."""
    fingerprint_manager = AdvancedFingerprintManager()
    profile = "desktop_chrome"
    if user_agent and "Firefox" in user_agent:
        profile = "desktop_firefox"
    elif user_agent and "Macintosh" in user_agent:
        profile = "mac_chrome"
    
    return await fingerprint_manager.create_stealth_browser_context(proxy, profile)
