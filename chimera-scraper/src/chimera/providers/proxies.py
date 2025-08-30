from abc import ABC, abstractmethod
from typing import List, Optional
import os
import random
from dotenv import load_dotenv

load_dotenv()

class ProxyProvider(ABC):
    """Abstract base class for proxy providers."""
    
    @abstractmethod
    async def get_proxy(self) -> Optional[str]:
        """Get a proxy URL."""
        pass

class StaticProxyProvider(ProxyProvider):
    """Provider that uses a static list of proxies."""
    
    def __init__(self):
        self.proxies = os.getenv("PROXY_LIST", "").split(",")
        self.current_index = 0
        
    async def get_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
            
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy if proxy else None

class LuminatiProxyProvider(ProxyProvider):
    """Provider for Bright Data (Luminati) proxies."""
    
    def __init__(self):
        self.username = os.getenv("LUMINATI_USERNAME")
        self.password = os.getenv("LUMINATI_PASSWORD")
        self.host = os.getenv("LUMINATI_HOST", "zproxy.lum-superproxy.io")
        self.port = os.getenv("LUMINATI_PORT", "22225")
        
    async def get_proxy(self) -> Optional[str]:
        if not all([self.username, self.password, self.host, self.port]):
            return None
            
        return f"http://{self.username}-session-rand{random.randint(1, 100000)}:{self.password}@{self.host}:{self.port}"
