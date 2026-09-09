#!/usr/bin/env python3
"""
My City Service - Advanced SEO/AEO/GEO Content Automation System
Production-Ready WordPress + DeepSeek AI Content Engine
"""

import os
import sys
import json
import time
import logging
import datetime
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==================================================
# LOGGING CONFIGURATION
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('content_publisher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==================================================
# ENVIRONMENT VARIABLES
# ==================================================

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# ==================================================
# COMPANY CONFIGURATION
# ==================================================

@dataclass
class CompanyConfig:
    name: str = "My City Service"
    tagline: str = "India's Trusted On-Demand Home Service Platform"
    website: str = "https://www.mycityservice.in"
    phone: str = "+91-9584670816"
    landline: str = "07692422904"
    email: str = "info@mycityservice.in"
    logo: str = "https://seoniservice.in/wp-content/uploads/2026/09/logo-mcs-1.png"
    
    # App Links
    playstore: str = "https://play.google.com/store/apps/details?id=com.myapp.sservices"
    appstore: str = "https://apps.apple.com/in/app/my-city-service/id6761624595"
    
    # Social Media
    social: Dict[str, str] = field(default_factory=lambda: {
        "instagram": "https://instagram.com/mycityservice.in",
        "facebook": "https://facebook.com/MyCityService",
        "linkedin": "https://linkedin.com/in/my-city-service",
        "twitter": "https://x.com/mycityservice9",
        "youtube": "https://youtube.com/@MyCityService",
        "pinterest": "https://pin.it/6WQE1XxYG",
        "whatsapp": "https://wa.me/919584670816",
        "whatsapp_channel": "https://whatsapp.com/channel/0029VbAbZ4M5K3zTCiDwsS2e",
        "arattai": "@my_city_service"
    })

COMPANY = CompanyConfig()

# ==================================================
# CITY CONFIGURATION (Scalable)
# ==================================================

@dataclass
class CityConfig:
    name: str
    slug: str
    region: str = "Madhya Pradesh"
    country: str = "India"
    
    # Local context hints for content generation
    local_hints: List[str] = field(default_factory=list)

CITIES: List[CityConfig] = [
    CityConfig(
        name="Seoni",
        slug="seoni",
        local_hints=["known for its natural beauty", "growing urban center"]
    ),
    CityConfig(
        name="Chhindwara",
        slug="chhindwara",
        local_hints=["major commercial hub", "rapidly developing city"]
    ),
    CityConfig(
        name="Jabalpur",
        slug="jabalpur",
        local_hints=["large city with diverse population", "major urban center"]
    ),
]

# ==================================================
# SERVICE CONFIGURATION (Rich metadata)
# ==================================================

@dataclass
class ServiceConfig:
    name_en: str
    name_hi: str
    slug: str
    category: str
    
    # Search intent
    primary_intent: str
    secondary_intents: List[str]
    
    # Customer pain points
    common_problems: List[str]
    
    # Related services
    related_services: List[str]
    
    # FAQ topics
    faq_topics: List[str]
    
    # Image placeholder (to be replaced with actual images)
    image_url: Optional[str] = None
    image_alt: Optional[str] = None
    
    # Semantic keywords
    semantic_keywords: List[str] = field(default_factory=list)
    
    # Long-tail variations
    long_tail_keywords: List[str] = field(default_factory=list)

SERVICES: List[ServiceConfig] = [
    ServiceConfig(
        name_en="Electrician",
        name_hi="इलेक्ट्रीशियन",
        slug="electrician",
        category="Home Services",
        primary_intent="local service discovery",
        secondary_intents=["emergency", "informational", "maintenance"],
        common_problems=[
            "frequent power outages",
            "faulty wiring",
            "fuse problems",
            "switchboard issues",
            "lighting problems"
        ],
        related_services=["Home Cleaning", "Appliance Repair"],
        faq_topics=[
            "electrician charges",
            "emergency electrician",
            "wiring safety",
            "switchboard repair"
        ],
        semantic_keywords=[
            "wiring", "fuse", "switchboard", "power outage",
            "electrical repair", "home electrical", "circuit"
        ],
        long_tail_keywords=[
            "electrician for home",
            "home electrician near me",
            "emergency electrical service"
        ]
    ),
    ServiceConfig(
        name_en="AC Repair",
        name_hi="एसी रिपेयर",
        slug="ac-repair",
        category="Home Services",
        primary_intent="transactional/local",
        secondary_intents=["problem-solving", "maintenance"],
        common_problems=[
            "AC not cooling",
            "AC gas leak",
            "AC water leakage",
            "AC making noise",
            "AC not starting"
        ],
        related_services=["Appliance Repair", "Water Purifier"],
        faq_topics=[
            "AC repair cost",
            "AC gas filling",
            "AC maintenance tips",
            "AC technician booking"
        ],
        semantic_keywords=[
            "cooling", "compressor", "gas filling", "thermostat",
            "split AC", "window AC", "AC service"
        ],
        long_tail_keywords=[
            "AC not cooling problem",
            "best AC repair service",
            "AC service at home"
        ]
    ),
    ServiceConfig(
        name_en="Plumber",
        name_hi="प्लम्बर",
        slug="plumber",
        category="Home Services",
        primary_intent="local service discovery",
        secondary_intents=["emergency", "informational"],
        common_problems=[
            "leaking pipes",
            "water taps leaking",
            "blocked drains",
            "toilet issues",
            "water pressure problems"
        ],
        related_services=["Home Cleaning"],
        faq_topics=[
            "plumbing charges",
            "emergency plumber",
            "pipe repair cost",
            "bathroom plumbing"
        ],
        semantic_keywords=[
            "pipes", "drain", "tap", "leakage",
            "bathroom", "kitchen", "plumbing"
        ],
        long_tail_keywords=[
            "plumber for home",
            "emergency plumber near me",
            "bathroom plumbing service"
        ]
    ),
    ServiceConfig(
        name_en="Home Cleaning",
        name_hi="होम क्लीनिंग",
        slug="home-cleaning",
        category="Cleaning Services",
        primary_intent="local service discovery",
        secondary_intents=["transactional", "maintenance"],
        common_problems=[
            "dust accumulation",
            "deep cleaning needed",
            "carpet stains",
            "kitchen grease",
            "bathroom cleaning"
        ],
        related_services=["Sofa Cleaning", "Carpet Cleaning"],
        faq_topics=[
            "home cleaning charges",
            "deep cleaning process",
            "cleaning team availability",
            "carpet cleaning service"
        ],
        semantic_keywords=[
            "dusting", "floor cleaning", "kitchen cleaning",
            "bathroom cleaning", "deep cleaning", "housekeeping"
        ],
        long_tail_keywords=[
            "home cleaning service at home",
            "deep cleaning for home",
            "regular housekeeping service"
        ]
    ),
    ServiceConfig(
        name_en="Appliance Repair",
        name_hi="अप्लायंस रिपेयर",
        slug="appliance-repair",
        category="Home Services",
        primary_intent="problem-solving",
        secondary_intents=["transactional", "informational"],
        common_problems=[
            "refrigerator not cooling",
            "washing machine issues",
            "microwave problems",
            "dishwasher not working",
            "fan not working"
        ],
        related_services=["AC Repair", "Electrician"],
        faq_topics=[
            "appliance repair cost",
            "warranty on repairs",
            "home appliance service",
            "technician booking"
        ],
        semantic_keywords=[
            "refrigerator", "washing machine", "microwave",
            "dishwasher", "appliance service", "home appliance"
        ],
        long_tail_keywords=[
            "refrigerator repair near me",
            "washing machine service",
            "home appliance repair"
        ]
    ),
    ServiceConfig(
        name_en="Carpenter",
        name_hi="कारपेंटर",
        slug="carpenter",
        category="Home Services",
        primary_intent="local service discovery",
        secondary_intents=["transactional", "informational"],
        common_problems=[
            "broken furniture",
            "door issues",
            "window problems",
            "cabinet repairs",
            "woodwork needed"
        ],
        related_services=["Painting"],
        faq_topics=[
            "carpenter charges",
            "furniture repair cost",
            "door repair service",
            "woodwork service"
        ],
        semantic_keywords=[
            "woodworking", "furniture", "cabinetry",
            "door", "window", "wood repair"
        ],
        long_tail_keywords=[
            "carpenter for home",
            "furniture repair near me",
            "woodwork service at home"
        ]
    ),
    ServiceConfig(
        name_en="Painting",
        name_hi="पेंटिंग",
        slug="painting",
        category="Home Services",
        primary_intent="transactional",
        secondary_intents=["informational", "maintenance"],
        common_problems=[
            "old paint cracking",
            "walls need painting",
            "water stains on walls",
            "exterior paint fading"
        ],
        related_services=["Carpenter", "Home Cleaning"],
        faq_topics=[
            "painting cost",
            "types of paint",
            "house painting process",
            "painting team service"
        ],
        semantic_keywords=[
            "painting", "walls", "exterior", "interior",
            "paint", "color", "texture"
        ],
        long_tail_keywords=[
            "home painting service",
            "house painting near me",
            "wall painting cost"
        ]
    ),
    ServiceConfig(
        name_en="Water Purifier",
        name_hi="वॉटर प्यूरीफायर",
        slug="water-purifier",
        category="Home Services",
        primary_intent="maintenance",
        secondary_intents=["informational", "transactional"],
        common_problems=[
            "water purifier not working",
            "water filter needs replacement",
            "taste issues",
            "water leakage"
        ],
        related_services=["Home Cleaning"],
        faq_topics=[
            "water purifier service",
            "filter replacement cost",
            "RO service",
            "water quality issues"
        ],
        semantic_keywords=[
            "purifier", "filter", "RO", "water quality",
            "taste", "service", "replacement"
        ],
        long_tail_keywords=[
            "water purifier repair near me",
            "RO filter replacement",
            "water purifier service at home"
        ]
    ),
    ServiceConfig(
        name_en="Sofa Cleaning",
        name_hi="सोफा क्लीनिंग",
        slug="sofa-cleaning",
        category="Cleaning Services",
        primary_intent="transactional",
        secondary_intents=["informational", "maintenance"],
        common_problems=[
            "sofa stains",
            "fabric dirt",
            "sofa odor",
            "pet stains",
            "deep cleaning needed"
        ],
        related_services=["Home Cleaning", "Carpet Cleaning"],
        faq_topics=[
            "sofa cleaning process",
            "sofa cleaning cost",
            "drying time",
            "fabric safety"
        ],
        semantic_keywords=[
            "sofa", "upholstery", "stains", "cleaning",
            "fabric", "deep clean", "vacuum"
        ],
        long_tail_keywords=[
            "sofa cleaning service at home",
            "upholstery cleaning near me",
            "sofa stain removal"
        ]
    ),
    ServiceConfig(
        name_en="Gas Stove Repair",
        name_hi="गैस स्टोव रिपेयर",
        slug="gas-stove-repair",
        category="Home Services",
        primary_intent="problem-solving",
        secondary_intents=["emergency", "transactional"],
        common_problems=[
            "gas stove not lighting",
            "flame issues",
            "burner problems",
            "gas leakage"
        ],
        related_services=["Appliance Repair"],
        faq_topics=[
            "gas stove repair cost",
            "burner repair",
            "safety check",
            "technician visit"
        ],
        semantic_keywords=[
            "burner", "flame", "gas", "stove",
            "ignition", "cooking", "kitchen"
        ],
        long_tail_keywords=[
            "gas stove repair near me",
            "gas burner service",
            "kitchen gas stove repair"
        ]
    ),
    ServiceConfig(
        name_en="Carpet Cleaning",
        name_hi="कार्पेट क्लीनिंग",
        slug="carpet-cleaning",
        category="Cleaning Services",
        primary_intent="transactional",
        secondary_intents=["informational", "maintenance"],
        common_problems=[
            "carpet stains",
            "dust accumulation",
            "carpet odor",
            "pet stains",
            "deep cleaning needed"
        ],
        related_services=["Sofa Cleaning", "Home Cleaning"],
        faq_topics=[
            "carpet cleaning process",
            "carpet cleaning cost",
            "drying time",
            "stain removal"
        ],
        semantic_keywords=[
            "carpet", "stains", "cleaning", "vacuum",
            "fabric", "deep clean", "odor"
        ],
        long_tail_keywords=[
            "carpet cleaning service at home",
            "carpet stain removal",
            "carpet deep cleaning"
        ]
    ),
    ServiceConfig(
        name_en="Commercial Cleaning",
        name_hi="कमर्शियल क्लीनिंग",
        slug="commercial-cleaning",
        category="Cleaning Services",
        primary_intent="transactional",
        secondary_intents=["informational", "maintenance"],
        common_problems=[
            "office cleaning",
            "warehouse cleaning",
            "industrial cleaning",
            "large space cleaning"
        ],
        related_services=["Home Cleaning"],
        faq_topics=[
            "commercial cleaning cost",
            "cleaning team size",
            "service schedule",
            "certified cleaning"
        ],
        semantic_keywords=[
            "commercial", "office", "warehouse",
            "industrial", "business", "large space"
        ],
        long_tail_keywords=[
            "office cleaning service",
            "commercial cleaning company",
            "business cleaning service"
        ]
    ),
    ServiceConfig(
        name_en="Pick & Drop Service",
        name_hi="पिक एंड ड्रॉप सर्विस",
        slug="pick-drop-service",
        category="Home Services",
        primary_intent="transactional",
        secondary_intents=["informational", "convenience"],
        common_problems=[
            "appliance transport",
            "heavy items",
            "home relocation",
            "item pick up"
        ],
        related_services=["Home Cleaning"],
        faq_topics=[
            "pick and drop charges",
            "service coverage",
            "item safety",
            "timing schedule"
        ],
        semantic_keywords=[
            "pickup", "delivery", "transport",
            "shift", "relocation", "heavy items"
        ],
        long_tail_keywords=[
            "pick and drop service near me",
            "home pickup service",
            "item transport service"
        ]
    ),
]

# ==================================================
# CITY-SERVICE AVAILABILITY MAP
# ==================================================

CITY_SERVICES: Dict[str, List[str]] = {
    "Seoni": [
        "Electrician", "AC Repair", "Plumber", "Home Cleaning",
        "Appliance Repair", "Carpenter", "Painting", "Water Purifier",
        "Sofa Cleaning", "Gas Stove Repair", "Carpet Cleaning",
        "Commercial Cleaning", "Pick & Drop Service"
    ],
    "Chhindwara": [
        "Electrician", "AC Repair", "Plumber", "Home Cleaning",
        "Appliance Repair", "Carpenter", "Painting", "Water Purifier",
        "Sofa Cleaning", "Gas Stove Repair", "Carpet Cleaning",
        "Commercial Cleaning", "Pick & Drop Service"
    ],
    "Jabalpur": [
        "Electrician", "AC Repair", "Plumber", "Home Cleaning",
        "Appliance Repair", "Carpenter", "Painting", "Water Purifier",
        "Sofa Cleaning", "Gas Stove Repair", "Carpet Cleaning",
        "Commercial Cleaning", "Pick & Drop Service"
    ],
}

# ==================================================
# SERVICE IMAGES (Configurable)
# ==================================================

SERVICE_IMAGES: Dict[str, Dict[str, str]] = {
    "Electrician": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/electrician-service.jpg",
        "alt": "Professional Electrician service at home"
    },
    "AC Repair": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/ac-repair-service.jpg",
        "alt": "AC Repair and service by trained technician"
    },
    "Plumber": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/plumber-service.jpg",
        "alt": "Professional Plumbing service at home"
    },
    "Home Cleaning": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/home-cleaning-service.jpg",
        "alt": "Home Cleaning service with trained staff"
    },
    "Appliance Repair": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/appliance-repair-service.jpg",
        "alt": "Appliance Repair service for all home appliances"
    },
    "Carpenter": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/carpenter-service.jpg",
        "alt": "Professional Carpenter service at home"
    },
    "Painting": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/painting-service.jpg",
        "alt": "Home Painting service with professional team"
    },
    "Water Purifier": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/water-purifier-service.jpg",
        "alt": "Water Purifier service and maintenance"
    },
    "Sofa Cleaning": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/sofa-cleaning-service.jpg",
        "alt": "Professional Sofa Cleaning service at home"
    },
    "Gas Stove Repair": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/gas-stove-repair-service.jpg",
        "alt": "Gas Stove Repair service at home"
    },
    "Carpet Cleaning": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/carpet-cleaning-service.jpg",
        "alt": "Professional Carpet Cleaning service at home"
    },
    "Commercial Cleaning": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/commercial-cleaning-service.jpg",
        "alt": "Commercial Cleaning service for businesses"
    },
    "Pick & Drop Service": {
        "url": "https://seoniservice.in/wp-content/uploads/2026/09/pick-drop-service.jpg",
        "alt": "Pick & Drop service for items and appliances"
    },
}

# ==================================================
# ARTICLE STRUCTURE TEMPLATES (For variation)
# ==================================================

class ArticleStructure(Enum):
    PROBLEM_SOLUTION = "problem_solution"
    LOCAL_NEED = "local_need"
    SYMPTOMS_CAUSES = "symptoms_causes"
    SERVICE_OVERVIEW = "service_overview"
    HOW_TO_GUIDE = "how_to_guide"
    MAINTENANCE_GUIDE = "maintenance_guide"
    COMPARISON = "comparison"
    EMERGENCY_GUIDE = "emergency_guide"

ARTICLE_STRUCTURES: Dict[ArticleStructure, Dict[str, List[str]]] = {
    ArticleStructure.PROBLEM_SOLUTION: {
        "sections": [
            "Introduction",
            "Common Problems with {service}",
            "How {service} Service Works",
            "Professional Service Benefits",
            "What Our {service} Service Includes",
            "Service Process",
            "Local Service Availability",
            "FAQs",
            "Book Your Service"
        ],
        "description": "Focus on common problems and how the service solves them"
    },
    ArticleStructure.LOCAL_NEED: {
        "sections": [
            "Introduction",
            "Why {city} Needs Professional {service} Services",
            "Common {service} Issues in {city}",
            "What to Expect from a Professional {service} Service",
            "Our {service} Service Approach",
            "Service Process",
            "Service Availability in {city}",
            "FAQs",
            "Book Your Service"
        ],
        "description": "Focus on local needs and specific requirements"
    },
    ArticleStructure.SYMPTOMS_CAUSES: {
        "sections": [
            "Introduction",
            "Common Symptoms That Indicate You Need {service} Service",
            "What Causes These Problems",
            "When to Call a Professional",
            "Our {service} Service Process",
            "Service Benefits",
            "Local Service Availability",
            "FAQs",
            "Book Your Service"
        ],
        "description": "Focus on symptoms, causes, and when to call a professional"
    },
    ArticleStructure.SERVICE_OVERVIEW: {
        "sections": [
            "Introduction",
            "Overview of {service} Services",
            "Common Customer Requests for {service}",
            "What Our {service} Service Includes",
            "Service Process",
            "Local Service Availability",
            "Why Choose Us for {service}",
            "FAQs",
            "Book Your Service"
        ],
        "description": "Focus on service overview and what customers typically request"
    },
    ArticleStructure.HOW_TO_GUIDE: {
        "sections": [
            "Introduction",
            "Understanding {service} Services",
            "How to Prepare for {service}",
            "The Service Process Explained",
            "What to Expect After Service",
            "Tips for Maintaining {service} in {city}",
            "Service Availability",
            "FAQs",
            "Book Your Service"
        ],
        "description": "Focus on step-by-step guidance and preparation"
    },
    ArticleStructure.MAINTENANCE_GUIDE: {
        "sections": [
            "Introduction",
            "Importance of Regular {service} Maintenance",
            "Common Maintenance Tasks",
            "Signs You Need Professional {service} Service",
            "Our Maintenance Service Process",
            "Service Benefits",
            "Service Availability in {city}",
            "FAQs",
            "Book Your Service"
        ],
        "description": "Focus on preventive maintenance and regular service"
    },
}

# ==================================================
# INTERNAL LINK CONFIGURATION
# ==================================================

INTERNAL_LINKS: Dict[str, Dict[str, str]] = {
    # City-specific service pages (if they exist)
    "seoni_ac_repair": {
        "url": "/seoni-ac-repair",
        "anchor": "AC Repair in Seoni",
        "context": "Learn more about our Seoni AC Repair service"
    },
    "seoni_plumber": {
        "url": "/seoni-plumber",
        "anchor": "Plumber in Seoni",
        "context": "Find expert plumbers in Seoni"
    },
    "seoni_home_cleaning": {
        "url": "/seoni-home-cleaning",
        "anchor": "Home Cleaning in Seoni",
        "context": "Get professional home cleaning in Seoni"
    },
    "jabalpur_ac_repair": {
        "url": "/jabalpur-ac-repair",
        "anchor": "AC Repair in Jabalpur",
        "context": "AC repair services in Jabalpur"
    },
    "jabalpur_plumber": {
        "url": "/jabalpur-plumber",
        "anchor": "Plumber in Jabalpur",
        "context": "Professional plumbers in Jabalpur"
    },
    "chhindwara_ac_repair": {
        "url": "/chhindwara-ac-repair",
        "anchor": "AC Repair in Chhindwara",
        "context": "AC repair services in Chhindwara"
    },
    "chhindwara_plumber": {
        "url": "/chhindwara-plumber",
        "anchor": "Plumber in Chhindwara",
        "context": "Professional plumbers in Chhindwara"
    },
    "home_services": {
        "url": "/",
        "anchor": "My City Service",
        "context": "Home services platform"
    },
    "app": {
        "url": "/app",
        "anchor": "Download App",
        "context": "Book services through the app"
    },
}

# ==================================================
# UTILITY FUNCTIONS
# ==================================================

def get_service_config(name: str) -> Optional[ServiceConfig]:
    """Get service configuration by name"""
    for service in SERVICES:
        if service.name_en == name:
            return service
    return None

def get_city_config(name: str) -> Optional[CityConfig]:
    """Get city configuration by name"""
    for city in CITIES:
        if city.name == name:
            return city
    return None

def get_service_image(service_name: str) -> Optional[Dict[str, str]]:
    """Get image configuration for a service"""
    return SERVICE_IMAGES.get(service_name)

def get_article_structure(service: ServiceConfig, city: CityConfig) -> ArticleStructure:
    """Select appropriate article structure based on service and city"""
    # Map service to structure type based on primary intent
    intent_mapping = {
        "problem-solving": ArticleStructure.SYMPTOMS_CAUSES,
        "transactional/local": ArticleStructure.SERVICE_OVERVIEW,
        "local service discovery": ArticleStructure.LOCAL_NEED,
        "maintenance": ArticleStructure.MAINTENANCE_GUIDE,
        "emergency": ArticleStructure.EMERGENCY_GUIDE,
        "how-to": ArticleStructure.HOW_TO_GUIDE,
        "comparison": ArticleStructure.COMPARISON,
    }
    
    # Get structure based on primary intent, fallback to PROBLEM_SOLUTION
    return intent_mapping.get(service.primary_intent, ArticleStructure.PROBLEM_SOLUTION)

def generate_seo_title(service: ServiceConfig, city: CityConfig, language: str = "en") -> str:
    """Generate SEO title"""
    if language == "hi":
        # Hindi title format
        return f"{city.name} में {service.name_hi} सेवा | ऑनलाइन बुक करें"
    else:
        # English title format
        if service.primary_intent in ["emergency", "problem-solving"]:
            return f"Best {service.name_en} Service in {city.name} | Book {service.name_en} Online"
        elif service.primary_intent == "maintenance":
            return f"Professional {service.name_en} Maintenance in {city.name} | Book Service"
        else:
            return f"{service.name_en} Service in {city.name} | Book Professional {service.name_en} Online"

def generate_meta_description(service: ServiceConfig, city: CityConfig, language: str = "en") -> str:
    """Generate meta description"""
    if language == "hi":
        return f"{city.name} में {service.name_hi} सेवा के लिए {COMPANY.name} पर भरोसा करें। हमारे अनुभवी प्रोफेशनल्स आपके घर पर आकर सेवा प्रदान करते हैं।"
    else:
        return f"Get trusted {service.name_en} services in {city.name} from {COMPANY.name}. Professional {service.name_en} at your doorstep. Book online now!"

def generate_slug(service: ServiceConfig, city: CityConfig) -> str:
    """Generate clean URL slug"""
    return f"{city.slug}-{service.slug}"

def get_hindi_keyword(service: ServiceConfig, city: CityConfig) -> str:
    """Generate Hindi keyword with correct city name"""
    return f"{city.name} में {service.name_hi}"

# ==================================================
# WORDPRESS API CLIENT
# ==================================================

class WordPressClient:
    def __init__(self, url: str, username: str, password: str):
        self.url = url.rstrip('/')
        self.auth = (username, password)
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def get_post_by_slug(self, slug: str) -> Optional[Dict]:
        """Check if a post with the given slug exists"""
        try:
            url = f"{self.url}/wp-json/wp/v2/posts"
            params = {"slug": slug, "status": "publish,draft"}
            response = self.session.get(url, params=params, auth=self.auth, timeout=30)
            if response.status_code == 200:
                posts = response.json()
                return posts[0] if posts else None
        except Exception as e:
            logger.error(f"Error checking post by slug: {e}")
        return None
    
    def get_category_id(self, category_name: str) -> int:
        """Get or create category by name"""
        try:
            url = f"{self.url}/wp-json/wp/v2/categories"
            slug = category_name.lower().replace(" ", "-").replace("&", "and")
            params = {"slug": slug}
            response = self.session.get(url, params=params, auth=self.auth, timeout=30)
            
            if response.status_code == 200 and response.json():
                return response.json()[0]["id"]
            
            # Create category if not exists
            data = {"name": category_name, "slug": slug}
            response = self.session.post(url, auth=self.auth, json=data, timeout=30)
            if response.status_code == 201:
                return response.json()["id"]
            return 1
        except Exception as e:
            logger.error(f"Error getting/creating category: {e}")
            return 1
    
    def get_tag_id(self, tag_name: str) -> Optional[int]:
        """Get or create tag by name"""
        try:
            url = f"{self.url}/wp-json/wp/v2/tags"
            params = {"search": tag_name}
            response = self.session.get(url, params=params, auth=self.auth, timeout=30)
            
            if response.status_code == 200 and response.json():
                return response.json()[0]["id"]
            
            # Create tag if not exists
            data = {"name": tag_name}
            response = self.session.post(url, auth=self.auth, json=data, timeout=30)
            if response.status_code == 201:
                return response.json()["id"]
        except Exception as e:
            logger.error(f"Error getting/creating tag: {e}")
        return None
    
    def create_post(self, post_data: Dict) -> Optional[Dict]:
        """Create a new post"""
        try:
            url = f"{self.url}/wp-json/wp/v2/posts"
            response = self.session.post(
                url, 
                auth=self.auth, 
                json=post_data,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                logger.error(f"WordPress API error: {response.status_code} - {response.text[:500]}")
                return None
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return None
    
    def update_post(self, post_id: int, post_data: Dict) -> Optional[Dict]:
        """Update an existing post"""
        try:
            url = f"{self.url}/wp-json/wp/v2/posts/{post_id}"
            response = self.session.post(
                url, 
                auth=self.auth, 
                json=post_data,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"WordPress API error: {response.status_code} - {response.text[:500]}")
                return None
        except Exception as e:
            logger.error(f"Error updating post: {e}")
            return None

# ==================================================
# DEEPSEEK API CLIENT
# ==================================================

class DeepSeekClient:
    def __init__(self, api_key: str, timeout: int = 60, max_retries: int = 3):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.url = "https://api.deepseek.com/v1/chat/completions"
    
    def generate_content(self, prompt: str) -> Optional[Dict]:
        """Generate content using DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": "Return ONLY valid JSON. No markdown formatting. No explanations."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 4500
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.url, 
                    headers=headers, 
                    json=data, 
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                content = response.json()["choices"][0]["message"]["content"]
                content = content.strip()
                
                # Clean JSON from markdown
                if content.startswith("```json"):
                    content = content[7:]
                elif content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                
                return json.loads(content)
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    # Try to salvage JSON with basic cleaning
                    try:
                        # Find JSON-like structure
                        start = content.find('{')
                        end = content.rfind('}') + 1
                        if start >= 0 and end > start:
                            cleaned = content[start:end]
                            return json.loads(cleaned)
                    except:
                        pass
                    return None
                time.sleep(2 ** attempt)
                
            except Exception as e:
                logger.error(f"DeepSeek API error (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    return None
                time.sleep(2 ** attempt)
        
        return None

# ==================================================
# CONTENT GENERATOR
# ==================================================

class ContentGenerator:
    def __init__(self, deepseek_client: DeepSeekClient):
        self.client = deepseek_client
    
    def _get_structure_sections(self, structure: ArticleStructure, service: ServiceConfig, city: CityConfig) -> List[str]:
        """Get section headers for a structure type"""
        template = ARTICLE_STRUCTURES.get(structure, ARTICLE_STRUCTURES[ArticleStructure.PROBLEM_SOLUTION])
        sections = template["sections"]
        
        # Replace placeholders
        return [
            section
            .replace("{service}", service.name_en)
            .replace("{city}", city.name)
            for section in sections
        ]
    
    def _get_structure_description(self, structure: ArticleStructure) -> str:
        """Get description of structure type"""
        template = ARTICLE_STRUCTURES.get(structure, ARTICLE_STRUCTURES[ArticleStructure.PROBLEM_SOLUTION])
        return template["description"]
    
    def _build_prompt(self, service: ServiceConfig, city: CityConfig, language: str = "en") -> str:
        """Build the prompt for DeepSeek"""
        structure = get_article_structure(service, city)
        sections = self._get_structure_sections(structure, service, city)
        structure_desc = self._get_structure_description(structure)
        
        focus_keyword = f"{service.name_en} in {city.name}" if language == "en" else f"{city.name} में {service.name_hi}"
        
        # Build problem list
        problems = ", ".join(service.common_problems[:4])
        
        # Build related services
        related = ", ".join(service.related_services[:2])
        
        # Build semantic keywords
        semantic_kw = ", ".join(service.semantic_keywords[:4])
        
        if language == "hi":
            return f"""आप '{COMPANY.name} - {COMPANY.tagline}' के लिए AI-first SEO, AEO & GEO विशेषज्ञ हैं।

{service.name_hi} सेवाओं के बारे में {city.name}, {city.region} के लिए एक AI-Optimized ब्लॉग पोस्ट लिखें।

**मुख्य कीवर्ड:** "{focus_keyword}"
**संरचना प्रकार:** {structure.value.replace('_', ' ').title()}
**संरचना विवरण:** {structure_desc}

**सख्त SEO नियम:**
1. मुख्य कीवर्ड को SEO शीर्षक, H1, परिचय, H2 में स्वाभाविक रूप से उपयोग करें
2. मेटा विवरण में कीवर्ड शामिल करें
3. पठनीयता को प्राथमिकता दें - कीवर्ड स्टफिंग न करें
4. प्राकृतिक भाषा का उपयोग करें
5. हर अनुभाग में वास्तविक जानकारी प्रदान करें
6. सामान्य कथनों से बचें

**व्यवसाय विवरण:**
- कंपनी: {COMPANY.name} ({COMPANY.tagline})
- फोन: {COMPANY.phone}
- वेबसाइट: {COMPANY.website}
- ऐप: {COMPANY.playstore}

**सेवा विवरण:**
- सामान्य समस्याएं: {problems}
- संबंधित सेवाएं: {related}
- अर्थवाचक कीवर्ड: {semantic_kw}

**अनुभाग संरचना:**
{chr(10).join(f'{i+1}. {section}' for i, section in enumerate(sections))}

**आउटपुट:** केवल वैध JSON लौटाएं।
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "focus_keyword": "{focus_keyword}",
    "quick_answer": "35-60 शब्दों में इस सेवा का प्रत्यक्ष उत्तर",
    "content_html": "",
    "faqs": [
        {{"question": "", "answer": ""}}
    ],
    "tags": ["टैग1", "टैग2", "टैग3", "टैग4", "टैग5"],
    "secondary_keywords": ["सेकेंडरी1", "सेकेंडरी2"],
    "search_intent": "",
    "article_type": "{structure.value}"
}}"""
        else:
            return f"""You are an AI-first SEO, AEO & GEO expert for '{COMPANY.name} - {COMPANY.tagline}'.

Write an AI-Optimized blog post about {service.name_en} services in {city.name}, {city.region}.

**Focus Keyword:** "{focus_keyword}"
**Structure Type:** {structure.value.replace('_', ' ').title()}
**Structure Description:** {structure_desc}

**Strict SEO Rules:**
1. Use focus keyword naturally in SEO title, H1, introduction, and H2 where natural
2. Include keyword in meta description
3. Prioritize readability - no keyword stuffing
4. Use natural language with transition words
5. Every section must provide actual information
6. Avoid generic statements

**Business Details:**
- Company: {COMPANY.name} ({COMPANY.tagline})
- Phone: {COMPANY.phone}
- Website: {COMPANY.website}
- App: {COMPANY.playstore}

**Service Details:**
- Common problems: {problems}
- Related services: {related}
- Semantic keywords: {semantic_kw}

**Section Structure:**
{chr(10).join(f'{i+1}. {section}' for i, section in enumerate(sections))}

**Output:** Return ONLY valid JSON.
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "focus_keyword": "{focus_keyword}",
    "quick_answer": "A direct answer in 35-60 words about this service",
    "content_html": "",
    "faqs": [
        {{"question": "", "answer": ""}}
    ],
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "secondary_keywords": ["secondary1", "secondary2"],
    "search_intent": "",
    "article_type": "{structure.value}"
}}"""
    
    def generate_article(self, service: ServiceConfig, city: CityConfig, language: str = "en") -> Optional[Dict]:
        """Generate article content"""
        prompt = self._build_prompt(service, city, language)
        logger.info(f"Generating {language} article for {service.name_en} in {city.name}")
        
        result = self.client.generate_content(prompt)
        
        if result:
            # Validate required fields
            required_fields = ["title", "meta_description", "slug", "focus_keyword", "quick_answer", "content_html", "faqs"]
            missing = [field for field in required_fields if not result.get(field)]
            
            if missing:
                logger.error(f"Missing required fields: {missing}")
                return None
            
            # Ensure FAQ has at least 4 items
            if not result.get("faqs") or len(result["faqs"]) < 4:
                logger.error("Insufficient FAQs generated")
                return None
            
            # Set slug if not provided
            if not result.get("slug"):
                result["slug"] = generate_slug(service, city)
            
            # Clean slug
            result["slug"] = result["slug"].lower().strip().replace(" ", "-")
            
            return result
        
        return None
    
    def generate_articles_with_variation(self, service: ServiceConfig, city: CityConfig, count: int = 2) -> List[Dict]:
        """Generate multiple articles with variations"""
        articles = []
        
        # Generate in English
        eng_article = self.generate_article(service, city, "en")
        if eng_article:
            articles.append(eng_article)
        
        # Generate in Hindi
        hin_article = self.generate_article(service, city, "hi")
        if hin_article:
            articles.append(hin_article)
        
        return articles

# ==================================================
# CONTENT VALIDATOR
# ==================================================

class ContentValidator:
    def __init__(self, service: ServiceConfig, city: CityConfig):
        self.service = service
        self.city = city
    
    def validate(self, article_data: Dict, language: str = "en") -> Tuple[bool, List[str]]:
        """Validate article content"""
        errors = []
        
        # 1. Check required fields
        required = ["title", "meta_description", "slug", "focus_keyword", "quick_answer", "content_html", "faqs"]
        for field in required:
            if not article_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # 2. Check title
        if article_data.get("title"):
            if len(article_data["title"]) < 20:
                errors.append("Title too short")
            if len(article_data["title"]) > 70:
                errors.append("Title too long (over 70 chars)")
        
        # 3. Check meta description
        if article_data.get("meta_description"):
            if len(article_data["meta_description"]) < 50:
                errors.append("Meta description too short")
            if len(article_data["meta_description"]) > 170:
                errors.append("Meta description too long (over 170 chars)")
        
        # 4. Check content
        if article_data.get("content_html"):
            if len(article_data["content_html"]) < 1000:
                errors.append("Content too short (less than 1000 chars)")
            
            # Check for placeholder text
            placeholders = ["lorem ipsum", "placeholder", "sample text", "dummy text", "test content"]
            content_lower = article_data["content_html"].lower()
            for placeholder in placeholders:
                if placeholder in content_lower:
                    errors.append(f"Contains placeholder text: {placeholder}")
        
        # 5. Check focus keyword
        if article_data.get("focus_keyword"):
            if language == "hi":
                expected = f"{self.city.name} में {self.service.name_hi}"
                if expected not in article_data["focus_keyword"]:
                    errors.append(f"Hindi focus keyword should contain '{expected}'")
            else:
                expected = f"{self.service.name_en} in {self.city.name}"
                if expected not in article_data["focus_keyword"]:
                    errors.append(f"Focus keyword should contain '{expected}'")
        
        # 6. Check FAQ count
        if article_data.get("faqs"):
            if len(article_data["faqs"]) < 4:
                errors.append("Need at least 4 FAQs")
        
        # 7. Check slug
        if article_data.get("slug"):
            if " " in article_data["slug"]:
                errors.append("Slug contains spaces")
            expected_slug = generate_slug(self.service, self.city)
            if article_data["slug"] != expected_slug:
                errors.append(f"Slug should be '{expected_slug}'")
        
        # 8. Check for internal links in content
        if article_data.get("content_html"):
            if not any(link in article_data["content_html"] for link in ["/", "mycityservice"]):
                errors.append("No internal links found in content")
        
        # 9. Check for company contact info
        if article_data.get("content_html"):
            if COMPANY.phone not in article_data["content_html"]:
                errors.append("Company phone number missing")
        
        return len(errors) == 0, errors

# ==================================================
# CONTENT PUBLISHER
# ==================================================

class ContentPublisher:
    def __init__(self, wp_client: WordPressClient, deepseek_client: DeepSeekClient):
        self.wp = wp_client
        self.generator = ContentGenerator(deepseek_client)
        self.published_posts = []
        self.skipped_posts = []
        self.failed_posts = []
    
    def _build_post_content(self, article_data: Dict, service: ServiceConfig, city: CityConfig, language: str = "en") -> str:
        """Build complete HTML content for WordPress"""
        content_parts = []
        
        # 1. Image (if available)
        image_config = get_service_image(service.name_en)
        if image_config:
            img_html = f'''
            <img src="{image_config['url']}" 
                 alt="{image_config['alt']} in {city.name}" 
                 title="{service.name_en} Service in {city.name}" 
                 style="max-width:100%;height:auto;" />
            <p><strong>Professional {service.name_en} Service in {city.name} by {COMPANY.name}</strong></p>
            '''
            content_parts.append(img_html)
        else:
            # Fallback to logo
            img_html = f'''
            <img src="{COMPANY.logo}" 
                 alt="{COMPANY.name}" 
                 title="{COMPANY.name}" 
                 style="max-width:100%;height:auto;" />
            '''
            content_parts.append(img_html)
        
        # 2. Quick Answer (AEO)
        if article_data.get("quick_answer"):
            quick_answer = f'''
            <div class="quick-answer" style="background:#f8f9fa;padding:15px;border-left:4px solid #ff6b00;margin:20px 0;">
                <h3>📌 Quick Answer</h3>
                <p>{article_data["quick_answer"]}</p>
            </div>
            '''
            content_parts.append(quick_answer)
        
        # 3. Main content
        content_parts.append(article_data["content_html"])
        
        # 4. FAQs
        if article_data.get("faqs"):
            faq_html = '<h2>Frequently Asked Questions (FAQs)</h2>'
            faq_html += '<div itemscope itemtype="https://schema.org/FAQPage">'
            for faq in article_data["faqs"]:
                faq_html += f'''
                <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
                    <h3 itemprop="name">Q: {faq["question"]}</h3>
                    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
                        <p itemprop="text">A: {faq["answer"]}</p>
                    </div>
                </div>
                '''
            faq_html += '</div>'
            content_parts.append(faq_html)
        
        # 5. Internal Links
        links_html = '<h2>Related Services</h2><ul>'
        for related in service.related_services:
            related_slug = related.lower().replace(" ", "-")
            city_slug = city.slug
            link_key = f"{city_slug}_{related_slug}"
            
            # Check if we have a configured link
            if link_key in INTERNAL_LINKS:
                link_data = INTERNAL_LINKS[link_key]
                if not link_data["url"].startswith("http"):
                    link_data["url"] = f"{COMPANY.website}{link_data['url']}"
                links_html += f'<li><a href="{link_data["url"]}" title="{link_data["context"]}">{link_data["anchor"]}</a></li>'
            else:
                # Use generic link
                generic_url = f"{COMPANY.website}/{city_slug}-{related_slug}"
                links_html += f'<li><a href="{generic_url}" title="{related} in {city.name}">{related} in {city.name}</a></li>'
        links_html += '</ul>'
        content_parts.append(links_html)
        
        # 6. CTA Section
        cta_html = f'''
        <div style="background:#f8f9fa;padding:20px;border-radius:8px;margin:30px 0;">
            <h2>📱 Book {service.name_en} Service in {city.name}</h2>
            <p><strong>{COMPANY.name}</strong> provides professional {service.name_en} services at your doorstep.</p>
            <p>📞 Call: <strong><a href="tel:{COMPANY.phone}">{COMPANY.phone}</a></strong></p>
            <p>📱 Download App: <a href="{COMPANY.playstore}">Android</a> | <a href="{COMPANY.appstore}">iOS</a></p>
            <p>🌐 Visit: <a href="{COMPANY.website}">{COMPANY.website}</a></p>
        </div>
        '''
        content_parts.append(cta_html)
        
        return '\n'.join(content_parts)
    
    def _build_post_data(self, article_data: Dict, service: ServiceConfig, city: CityConfig, language: str = "en") -> Dict:
        """Build WordPress post data"""
        # Get category
        category_name = service.category
        if language == "hi":
            category_name = f"{category_name} - Hindi"
        category_id = self.wp.get_category_id(category_name)
        
        # Get tags
        tag_ids = []
        tags = article_data.get("tags", [])
        if not tags:
            tags = [service.name_en, city.name, service.category]
        
        for tag in tags[:5]:
            tag_id = self.wp.get_tag_id(tag)
            if tag_id:
                tag_ids.append(tag_id)
        
        # Build content
        content = self._build_post_content(article_data, service, city, language)
        
        # Build post data
        post_data = {
            "title": article_data["title"],
            "content": content,
            "status": "publish",
            "slug": article_data["slug"],
            "categories": [category_id],
            "tags": tag_ids,
        }
        
        # Add Yoast meta data if available
        if article_data.get("meta_description"):
            post_data["meta"] = {
                "_yoast_wpseo_metadesc": article_data["meta_description"],
                "_yoast_wpseo_title": article_data["title"],
                "_yoast_wpseo_focuskw": article_data.get("focus_keyword", ""),
            }
        
        return post_data
    
    def publish_article(self, service: ServiceConfig, city: CityConfig, language: str = "en") -> Optional[Dict]:
        """Generate and publish a single article"""
        # Check if article already exists
        slug = generate_slug(service, city)
        existing_post = self.wp.get_post_by_slug(slug)
        
        if existing_post:
            logger.info(f"⏭️  Skipping {service.name_en} in {city.name} - post already exists")
            self.skipped_posts.append({
                "service": service.name_en,
                "city": city.name,
                "slug": slug,
                "reason": "Post already exists"
            })
            return existing_post
        
        # Generate article
        article_data = self.generator.generate_article(service, city, language)
        if not article_data:
            logger.error(f"❌ Failed to generate article for {service.name_en} in {city.name}")
            self.failed_posts.append({
                "service": service.name_en,
                "city": city.name,
                "reason": "Generation failed"
            })
            return None
        
        # Validate article
        validator = ContentValidator(service, city)
        is_valid, errors = validator.validate(article_data, language)
        
        if not is_valid:
            logger.error(f"❌ Validation failed for {service.name_en} in {city.name}: {errors}")
            self.failed_posts.append({
                "service": service.name_en,
                "city": city.name,
                "reason": f"Validation failed: {errors}"
            })
            return None
        
        # Build post data
        post_data = self._build_post_data(article_data, service, city, language)
        
        # Publish
        result = self.wp.create_post(post_data)
        if result:
            logger.info(f"✅ Published: {article_data['title']} (ID: {result.get('id')})")
            self.published_posts.append({
                "service": service.name_en,
                "city": city.name,
                "title": article_data["title"],
                "post_id": result.get("id"),
                "url": result.get("link")
            })
            return result
        else:
            logger.error(f"❌ Failed to publish {service.name_en} in {city.name}")
            self.failed_posts.append({
                "service": service.name_en,
                "city": city.name,
                "reason": "WordPress publish failed"
            })
            return None
    
    def publish_multiple(self, service: ServiceConfig, city: CityConfig) -> List[Dict]:
        """Publish both English and Hindi versions"""
        results = []
        
        # Publish English
        result_en = self.publish_article(service, city, "en")
        if result_en:
            results.append(result_en)
        
        # Publish Hindi
        result_hi = self.publish_article(service, city, "hi")
        if result_hi:
            results.append(result_hi)
        
        return results
    
    def generate_publishing_plan(self) -> List[Dict[str, Any]]:
        """Generate a publishing plan based on city-service availability"""
        plan = []
        
        for city in CITIES:
            available_services = CITY_SERVICES.get(city.name, [])
            for service_name in available_services:
                service = get_service_config(service_name)
                if service:
                    plan.append({
                        "city": city,
                        "service": service,
                        "slug": generate_slug(service, city)
                    })
        
        return plan
    
    def run_publishing_batch(self, limit: Optional[int] = None) -> Dict:
        """Run a batch publishing session"""
        plan = self.generate_publishing_plan()
        
        # Shuffle to vary publishing order
        import random
        random.shuffle(plan)
        
        if limit:
            plan = plan[:limit]
        
        logger.info(f"📋 Publishing plan: {len(plan)} articles")
        
        for item in plan:
            service = item["service"]
            city = item["city"]
            
            # Check if already published
            existing = self.wp.get_post_by_slug(item["slug"])
            if existing:
                logger.info(f"⏭️ Skipping {service.name_en} in {city.name} - already published")
                continue
            
            # Publish
            self.publish_multiple(service, city)
            
            # Delay between articles
            time.sleep(3)
        
        return {
            "published": len(self.published_posts),
            "skipped": len(self.skipped_posts),
            "failed": len(self.failed_posts),
            "details": {
                "published_posts": self.published_posts,
                "skipped_posts": self.skipped_posts,
                "failed_posts": self.failed_posts
            }
        }

# ==================================================
# MAIN EXECUTION
# ==================================================

def main():
    """Main execution function"""
    logger.info("🚀 Starting My City Service Content Automation System")
    
    # Validate environment variables
    if not all([DEEPSEEK_API_KEY, WP_URL, WP_USERNAME, WP_APP_PASSWORD]):
        logger.error("❌ Missing environment variables. Please set:")
        logger.error("  - DEEPSEEK_API_KEY")
        logger.error("  - WP_URL")
        logger.error("  - WP_USERNAME")
        logger.error("  - WP_APP_PASSWORD")
        sys.exit(1)
    
    # Initialize clients
    wp_client = WordPressClient(WP_URL, WP_USERNAME, WP_APP_PASSWORD)
    deepseek_client = DeepSeekClient(DEEPSEEK_API_KEY)
    publisher = ContentPublisher(wp_client, deepseek_client)
    
    # Run publishing
    result = publisher.run_publishing_batch(limit=2)  # Publish 2 services (English + Hindi = 4 posts)
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📊 PUBLISHING SUMMARY")
    logger.info("="*50)
    logger.info(f"✅ Published: {result['published']} posts")
    logger.info(f"⏭️  Skipped: {result['skipped']} posts")
    logger.info(f"❌ Failed: {result['failed']} posts")
    
    if result['published'] > 0:
        logger.info("\n📝 Published Posts:")
        for post in result['details']['published_posts']:
            logger.info(f"  - {post['title']} ({post['city']})")
            logger.info(f"    URL: {post['url']}")
    
    if result['failed'] > 0:
        logger.info("\n❌ Failed Posts:")
        for post in result['details']['failed_posts']:
            logger.info(f"  - {post['service']} in {post['city']}")
            logger.info(f"    Reason: {post['reason']}")
    
    logger.info("\n✅ Content automation completed!")

if __name__ == "__main__":
    main()
