#!/usr/bin/env python3
"""
My City Service - Fixed Production Script for GitHub Actions
"""

import os
import sys
import json
import requests
import datetime
import logging

# ==================================================
# LOGGING - GitHub Actions ke liye important
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
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

if not all([DEEPSEEK_API_KEY, WP_URL, WP_USERNAME, WP_APP_PASSWORD]):
    logger.error("❌ Missing environment variables!")
    logger.error("Please set: DEEPSEEK_API_KEY, WP_URL, WP_USERNAME, WP_APP_PASSWORD")
    sys.exit(1)

logger.info(f"✅ WP_URL: {WP_URL}")
logger.info(f"✅ WP_USERNAME: {WP_USERNAME}")

# ==================================================
# COMPANY DETAILS
# ==================================================

COMPANY_NAME = "My City Service"
COMPANY_TAGLINE = "India's Trusted On-Demand Home Service Platform"
COMPANY_PHONE = "+91-9584670816"
COMPANY_LANDLINE = "07692422904"
COMPANY_EMAIL = "info@mycityservice.in"
COMPANY_WEBSITE = "https://www.mycityservice.in"
LOGO_URL = "https://seoniservice.in/wp-content/uploads/2026/09/logo-mcs-1.png"

SOCIAL_LINKS = {
    "website": COMPANY_WEBSITE,
    "twitter": "https://x.com/mycityservice9",
    "instagram": "https://instagram.com/mycityservice.in",
    "facebook": "https://facebook.com/MyCityService",
    "linkedin": "https://linkedin.com/in/my-city-service",
    "whatsapp": "https://wa.me/919584670816",
    "whatsapp_channel": "https://whatsapp.com/channel/0029VbAbZ4M5K3zTCiDwsS2e",
    "youtube": "https://youtube.com/@MyCityService",
    "pinterest": "https://pin.it/6WQE1XxYG",
    "arattai": "@my_city_service",
    "playstore": "https://play.google.com/store/apps/details?id=com.myapp.sservices",
    "appstore": "https://apps.apple.com/in/app/my-city-service/id6761624595"
}

# ==================================================
# CITIES & SERVICES
# ==================================================

CITIES = [
    {"name": "Seoni", "slug": "seoni"},
    {"name": "Chhindwara", "slug": "chhindwara"},
    {"name": "Jabalpur", "slug": "jabalpur"}
]

SERVICE_NAMES = [
    {"name": "Electrician", "category": "Electrician"},
    {"name": "AC Repair", "category": "AC-Service"},
    {"name": "Plumber", "category": "Plumber"},
    {"name": "Home Cleaning", "category": "Cleaning-Services"},
    {"name": "Appliance Repair", "category": "Appliance-Repair"},
    {"name": "Carpenter", "category": "Carpenter"},
    {"name": "Painting", "category": "Painting-Services"},
    {"name": "Water Purifier", "category": "Water-Purifier"},
    {"name": "Sofa Cleaning", "category": "Sofa-Cleaning"},
    {"name": "Gas Stove Repair", "category": "Gas-Stove-Repair"},
    {"name": "Carpet Cleaning", "category": "Carpet-Cleaning"},
    {"name": "Commercial Cleaning", "category": "Commercial-Cleaning"},
    {"name": "Pick & Drop Service", "category": "Pick-Drop-Service"}
]

SERVICES = []
for city in CITIES:
    for service in SERVICE_NAMES:
        SERVICES.append({
            "name": service["name"],
            "category": f"{city['name']}-{service['category']}",
            "city": city["name"],
            "keyword": f"{service['name']} in {city['name']}",
            "slug": f"{service['name'].lower().replace(' ', '-')}-{city['slug']}"
        })

# ==================================================
# HINDI TRANSLATIONS
# ==================================================

SERVICES_HI = {
    "Electrician": "इलेक्ट्रीशियन", "AC Repair": "एसी रिपेयर", "Plumber": "प्लम्बर",
    "Home Cleaning": "होम क्लीनिंग", "Appliance Repair": "अप्लायंस रिपेयर", "Carpenter": "कारपेंटर",
    "Painting": "पेंटिंग", "Water Purifier": "वॉटर प्यूरीफायर", "Sofa Cleaning": "सोफा क्लीनिंग",
    "Gas Stove Repair": "गैस स्टोव रिपेयर", "Carpet Cleaning": "कार्पेट क्लीनिंग", "Commercial Cleaning": "कमर्शियल क्लीनिंग",
    "Pick & Drop Service": "पिक एंड ड्रॉप सर्विस"
}

def get_hindi_keyword(service_name, city_name):
    service_hi = SERVICES_HI.get(service_name, service_name)
    return f"{city_name} में {service_hi}"

# ==================================================
# WORDPRESS API FUNCTIONS
# ==================================================

def get_category_id(category_name):
    try:
        url = f"{WP_URL}/wp-json/wp/v2/categories"
        slug = category_name.lower().replace(" ", "-").replace("&", "and")
        params = {"slug": slug}
        response = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD), timeout=30)
        
        if response.status_code == 200 and response.json():
            return response.json()[0]["id"]
        
        data = {"name": category_name, "slug": slug}
        response = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=data, timeout=30)
        if response.status_code == 201:
            return response.json()["id"]
        
        logger.warning(f"Using default category ID 1 for: {category_name}")
        return 1
    except Exception as e:
        logger.error(f"Category error: {e}")
        return 1

def check_post_exists(slug):
    try:
        url = f"{WP_URL}/wp-json/wp/v2/posts"
        params = {"slug": slug, "status": "publish,draft"}
        response = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD), timeout=30)
        if response.status_code == 200:
            posts = response.json()
            return len(posts) > 0
    except Exception as e:
        logger.error(f"Error checking post: {e}")
    return False

# ==================================================
# DEEPSEEK CONTENT GENERATION
# ==================================================

def generate_blog_post(service_name, keyword, city, language="en"):
    service_hi = SERVICES_HI.get(service_name, service_name)
    keyword_hi = get_hindi_keyword(service_name, city)
    
    if language == "hi":
        prompt = f"""आप '{COMPANY_NAME} - {COMPANY_TAGLINE}' के लिए SEO विशेषज्ञ हैं।

{service_hi} सेवाओं के बारे में {city}, मध्य प्रदेश के लिए एक ब्लॉग पोस्ट लिखें।

मुख्य कीवर्ड: "{keyword_hi}"

नियम:
1. कीवर्ड को SEO शीर्षक, मेटा विवरण, और H1 में उपयोग करें
2. पठनीयता को प्राथमिकता दें - कीवर्ड स्टफिंग न करें
3. प्राकृतिक भाषा का उपयोग करें
4. हर अनुभाग में वास्तविक जानकारी प्रदान करें

व्यवसाय विवरण:
- कंपनी: {COMPANY_NAME} ({COMPANY_TAGLINE})
- फोन: {COMPANY_PHONE}
- वेबसाइट: {COMPANY_WEBSITE}
- ऐप: {SOCIAL_LINKS['playstore']}

अनुभाग:
1. परिचय
2. सेवा विवरण
3. लाभ
4. सेवा प्रक्रिया
5. FAQs (कम से कम 5)
6. Call to Action

आउटपुट: केवल वैध JSON
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "content_html": "",
    "faqs": [{{"question": "", "answer": ""}}],
    "tags": ["टैग1", "टैग2", "टैग3"]
}}
"""
    else:
        prompt = f"""You are an SEO expert for '{COMPANY_NAME} - {COMPANY_TAGLINE}'.

Write a blog post about {service_name} services in {city}, Madhya Pradesh.

Focus Keyword: "{keyword}"

Rules:
1. Use keyword naturally in SEO title, meta description, and H1
2. Prioritize readability - no keyword stuffing
3. Use natural language
4. Every section must provide actual information

Business Details:
- Company: {COMPANY_NAME} ({COMPANY_TAGLINE})
- Phone: {COMPANY_PHONE}
- Website: {COMPANY_WEBSITE}
- App: {SOCIAL_LINKS['playstore']}

Sections:
1. Introduction
2. Service Overview
3. Benefits
4. Service Process
5. FAQs (at least 5)
6. Call to Action

Output: ONLY valid JSON
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "content_html": "",
    "faqs": [{{"question": "", "answer": ""}}],
    "tags": ["tag1", "tag2", "tag3"]
}}
"""

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Return ONLY valid JSON. No markdown."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 4000
    }
    
    try:
        logger.info(f"Generating {language} content for {service_name} in {city}")
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        content = response.json()["choices"][0]["message"]["content"]
        content = content.strip()
        
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        result = json.loads(content)
        logger.info(f"✅ Generated {language} content for {service_name} in {city}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Generation error for {service_name} in {city}: {e}")
        return None

# ==================================================
# WORDPRESS PUBLISHING
# ==================================================

def publish_to_wordpress(blog_data, service_info):
    if not blog_data:
        logger.error("No blog data to publish")
        return None
    
    slug = blog_data.get("slug", service_info["slug"])
    if check_post_exists(slug):
        logger.info(f"⏭️ Skipping {service_info['name']} in {service_info['city']} - already published")
        return {"status": "skipped", "reason": "Already exists"}

    full_content = blog_data.get("content_html", "")
    
    if blog_data.get("meta_description"):
        ai_summary = f"<p><strong>Quick Answer:</strong> {blog_data['meta_description']}</p>"
        full_content = ai_summary + full_content

    if blog_data.get("faqs"):
        faq_html = "<h2>Frequently Asked Questions</h2>"
        for faq in blog_data["faqs"]:
            faq_html += f'<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">'
            faq_html += f'<h3 itemprop="name">Q: {faq["question"]}</h3>'
            faq_html += f'<div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">'
            faq_html += f'<p itemprop="text">A: {faq["answer"]}</p></div></div>'
        full_content += faq_html

    image_html = f'''
    <img src="{LOGO_URL}" style="max-width:100%;" alt="{service_info['keyword']} - {COMPANY_NAME}" />
    <p><strong>Trusted {service_info['name']} Services in {service_info['city']} by {COMPANY_NAME}.</strong></p>
    '''
    full_content = image_html + full_content

    cta_html = f'''
    <div style="background:#f8f9fa;padding:20px;border-radius:8px;margin:30px 0;">
        <h2>📱 Book {service_info['name']} Service in {service_info['city']}</h2>
        <p><strong>{COMPANY_NAME}</strong> provides professional {service_info['name']} services.</p>
        <p>📞 Call: <strong><a href="tel:{COMPANY_PHONE}">{COMPANY_PHONE}</a></strong></p>
        <p>📱 Download App: <a href="{SOCIAL_LINKS['playstore']}">Android</a></p>
        <p>🌐 Visit: <a href="{COMPANY_WEBSITE}">{COMPANY_WEBSITE}</a></p>
    </div>
    '''
    full_content += cta_html

    category_id = get_category_id(service_info["category"])
    
    tag_ids = []
    if blog_data.get("tags"):
        for tag_name in blog_data["tags"][:5]:
            try:
                url = f"{WP_URL}/wp-json/wp/v2/tags"
                params = {"search": tag_name}
                response = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD), timeout=30)
                if response.status_code == 200 and response.json():
                    tag_ids.append(response.json()[0]["id"])
                else:
                    data = {"name": tag_name}
                    response = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=data, timeout=30)
                    if response.status_code == 201:
                        tag_ids.append(response.json()["id"])
            except Exception as e:
                logger.error(f"Tag error for {tag_name}: {e}")

    wp_api_url = f"{WP_URL}/wp-json/wp/v2/posts"
    post_data = {
        "title": blog_data["title"],
        "content": full_content,
        "status": "publish",
        "slug": slug,
        "categories": [category_id],
        "tags": tag_ids,
        "meta": {
            "_yoast_wpseo_metadesc": blog_data.get("meta_description", ""),
            "_yoast_wpseo_title": blog_data["title"],
            "_yoast_wpseo_focuskw": service_info.get("keyword", service_info["name"])
        }
    }

    try:
        logger.info(f"📤 Publishing to WordPress: {blog_data['title']}")
        response = requests.post(wp_api_url, auth=(WP_USERNAME, WP_APP_PASSWORD), 
                                 json=post_data, headers={"Content-Type": "application/json"}, timeout=60)
        
        if response.status_code == 201:
            result = response.json()
            logger.info(f"✅ Published: {blog_data['title']}")
            logger.info(f"   URL: {result.get('link', '')}")
            logger.info(f"   Post ID: {result.get('id')}")
            return result
        else:
            logger.error(f"❌ WordPress Error: {response.status_code}")
            logger.error(f"   Response: {response.text[:500]}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Publishing error: {e}")
        return None

# ==================================================
# MAIN EXECUTION
# ==================================================

def main():
    logger.info("🚀 Starting My City Service Content Automation")
    logger.info("="*50)
    
    day_index = datetime.datetime.now().day % len(SERVICES)
    service1 = SERVICES[day_index]
    service2 = SERVICES[(day_index + 1) % len(SERVICES)]
    
    logger.info(f"📋 Today's services:")
    logger.info(f"   Service 1: {service1['name']} in {service1['city']}")
    logger.info(f"   Service 2: {service2['name']} in {service2['city']}")
    logger.info("="*50)
    
    published_count = 0
    skipped_count = 0
    failed_count = 0
    
    for service in [service1, service2]:
        logger.info(f"\n📝 Generating English post for {service['name']} in {service['city']}")
        data = generate_blog_post(service["name"], service["keyword"], service["city"], "en")
        if data:
            result = publish_to_wordpress(data, service)
            if result:
                if result.get("status") == "skipped":
                    skipped_count += 1
                else:
                    published_count += 1
            else:
                failed_count += 1
        else:
            failed_count += 1
    
    for service in [service1, service2]:
        hindi_keyword = get_hindi_keyword(service["name"], service["city"])
        logger.info(f"\n📝 Generating Hindi post for {service['name']} in {service['city']}")
        
        data_hi = generate_blog_post(service["name"], service["keyword"], service["city"], "hi")
        if data_hi:
            service_hi = service.copy()
            service_hi["category"] = service["category"] + "-HI"
            service_hi["keyword"] = hindi_keyword
            result = publish_to_wordpress(data_hi, service_hi)
            if result:
                if result.get("status") == "skipped":
                    skipped_count += 1
                else:
                    published_count += 1
            else:
                failed_count += 1
        else:
            failed_count += 1
    
    logger.info("\n" + "="*50)
    logger.info("📊 PUBLISHING SUMMARY")
    logger.info("="*50)
    logger.info(f"✅ Published: {published_count}")
    logger.info(f"⏭️  Skipped: {skipped_count}")
    logger.info(f"❌ Failed: {failed_count}")
    logger.info("\n✅ Content automation completed!")

if __name__ == "__main__":
    main()
