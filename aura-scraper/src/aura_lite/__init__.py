"""
AURA-LITE - Specialized Capterra Scraper
Adapted from Chimera-Ultimate for targeted review platform scraping
"""

from .aura_lite import AuraLite
from .core.cloudflare_bypass import CloudflareBypassManager
from .core.human_behavior import HumanBehaviorSimulator
from .managers.target_manager import CapterraTargetManager
from .managers.session_manager import SessionManager
from .extractors.data_extractor import CapterraDataExtractor

__version__ = "1.0.0"
__author__ = "AURA-LITE Team"

__all__ = [
    'AuraLite',
    'CloudflareBypassManager',
    'HumanBehaviorSimulator',
    'CapterraTargetManager',
    'SessionManager',
    'CapterraDataExtractor'
]
