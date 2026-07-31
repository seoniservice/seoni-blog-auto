import os
import json
import requests
import datetime

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# ===== COMPANY DETAILS =====
COMPANY_NAME = "My City Service"
COMPANY_PHONE = "+91-9584670816"
COMPANY_LANDLINE = "07692422904"
COMPANY_EMAIL = "info@mycityservice.in"
COMPANY_WEBSITE = "https://www.mycityservice.in"

# ===== SOCIAL MEDIA LINKS =====
SOCIAL_LINKS = {
    "website": "https://www.mycityservice.in",
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

# ===== SERVICES LIST =====
SERVICES = [
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

def get_category_id(category_name):
    try:
        url = f"{WP_URL}/wp-json/wp/v2/categories"
        params = {"slug": category_name.lower().replace(" ", "-").replace("&", "and")}
        response = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD))
        if response.status_code == 200 and response.json():
            return response.json()[0]["id"]
        data = {"name": category_name, "slug": category_name.lower().replace(" ", "-").replace("&", "and")}
        response = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=data)
        if response.status_code == 201:
            return response.json()["id"]
        return 1
    except:
        return 1

def generate_blog_post(service_name):
    prompt = f"""You are an expert Senior SEO, GEO, AEO, and Local Content Strategist for '{COMPANY_NAME}' ({COMPANY_WEBSITE}).

Write a comprehensive SEO-optimized blog post about {service_name} services in Seoni, Madhya Pradesh.

IMPORTANT: Use these EXACT contact details:
- Company: {COMPANY_NAME}
- Phone: {COMPANY_PHONE}
- Landline: {COMPANY_LANDLINE}
- Email: {COMPANY_EMAIL}
- Website: {COMPANY_WEBSITE}
- WhatsApp: {SOCIAL_LINKS['whatsapp']}
- Instagram: {SOCIAL_LINKS['instagram']}
- YouTube: {SOCIAL_LINKS['youtube']}
- LinkedIn: {SOCIAL_LINKS['linkedin']}
- Facebook: {SOCIAL_LINKS['facebook']}
- Twitter/X: {SOCIAL_LINKS['twitter']}
- Pinterest: {SOCIAL_LINKS['pinterest']}
- Arattai: {SOCIAL_LINKS['arattai']}
- Android App: {SOCIAL_LINKS['playstore']}
- iOS App: {SOCIAL_LINKS['appstore']}

STRUCTURE MUST INCLUDE:
1. SEO Metadata: Catchy title (under 60 chars), meta description (under 160 chars with CTA), SEO-friendly slug
2. Introduction with local Seoni intent and common pain points
3. Why Choose {COMPANY_NAME}: Local reliability, verified technicians, transparent pricing, quick response
4. Comprehensive Service Overview: What the service includes, key features, benefits
5. Pricing & Process: Transparent rates, step-by-step process with correct phone number
6. Tools, Safety & Maintenance: Equipment used, DIY vs Professional comparison
7. Local Service Areas: Main Road, Subhash Ward, Barapatthar, and nearby MP regions
8. FAQs (7-10 questions with answers) - Must include schema-ready FAQ content
9. Strong Call to Action with all contact details and app download links

Make content readable with proper H2, H3 headings, short paragraphs, and bullet points.
Optimize for Google Search, AI Search (Perplexity, ChatGPT, Gemini), and Voice Search.

OUTPUT FORMAT: Return valid JSON only:
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "content_html": "",
    "faqs": [{{"question": "", "answer": ""}}],
    "tags": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}
"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": "Return valid JSON only. Always include 7-10 FAQs."}, {"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 5000
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        print(f"❌ DeepSeek Error: {e}")
        return None

def publish_to_wordpress(blog_data, service_info):
    if not blog_data:
        return None

    full_content = blog_data["content_html"]
    if blog_data.get("faqs"):
        faq_html = "<h2>Frequently Asked Questions (FAQs)</h2>"
        for faq in blog_data["faqs"]:
            faq_html += f'<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><h3 itemprop="name">Q: {faq["question"]}</h3><div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">A: {faq["answer"]}</p></div></div>'
        full_content += faq_html

    # Social Media & Contact Section
    social_html = f"""
    <h2>📱 Connect With {COMPANY_NAME}</h2>
    <p>Follow us on social media for updates and offers:</p>
    <ul>
        <li>🌐 <a href="{SOCIAL_LINKS['website']}">Website</a></li>
        <li>📱 <a href="{SOCIAL_LINKS['whatsapp']}">WhatsApp</a></li>
        <li>📸 <a href="{SOCIAL_LINKS['instagram']}">Instagram</a></li>
        <li>▶️ <a href="{SOCIAL_LINKS['youtube']}">YouTube</a></li>
        <li>💼 <a href="{SOCIAL_LINKS['linkedin']}">LinkedIn</a></li>
        <li>📘 <a href="{SOCIAL_LINKS['facebook']}">Facebook</a></li>
        <li>🐦 <a href="{SOCIAL_LINKS['twitter']}">Twitter/X</a></li>
        <li>📌 <a href="{SOCIAL_LINKS['pinterest']}">Pinterest</a></li>
        <li>💬 <a href="{SOCIAL_LINKS['arattai']}">Arattai</a></li>
    </ul>

    <h2>📲 Download Our App</h2>
    <ul>
        <li>📱 <a href="{SOCIAL_LINKS['playstore']}">Android (Play Store)</a></li>
        <li>🍎 <a href="{SOCIAL_LINKS['appstore']}">iPhone (App Store)</a></li>
    </ul>

    <h2>📞 Contact Us</h2>
    <p>📞 Call: <strong>{COMPANY_PHONE}</strong></p>
    <p>🏠 Landline: <strong>{COMPANY_LANDLINE}</strong></p>
    <p>📧 Email: <strong>{COMPANY_EMAIL}</strong></p>
    <p>🌐 Website: <strong>{COMPANY_WEBSITE}</strong></p>
    """
    full_content += social_html

    category_id = get_category_id(service_info["category"])
    tag_ids = []
    if blog_data.get("tags"):
        for tag_name in blog_data["tags"][:5]:
            tag_id = get_or_create_tag(tag_name)
            if tag_id:
                tag_ids.append(tag_id)

    wp_api_url = f"{WP_URL}/wp-json/wp/v2/posts"
    post_data = {
        "title": blog_data["title"],
        "content": full_content,
        "status": "publish",
        "slug": blog_data["slug"],
        "categories": [category_id],
        "tags": tag_ids,
        "meta": {
            "_yoast_wpseo_metadesc": blog_data.get("meta_description", ""),
            "_yoast_wpseo_title": blog_data["title"],
            "_yoast_wpseo_focuskw": service_info["name"]
        }
    }

    try:
        response = requests.post(wp_api_url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=post_data, headers={"Content-Type": "application/json"})
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Published: {blog_data['title']}")
            print(f"   URL: {result.get('link', '')}")
            print(f"   Category: {service_info['category']}")
            return result
        else:
            print(f"❌ WordPress Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_or_create_tag(tag_name):
    try:
        url = f"{WP_URL}/wp-json/wp/v2/tags"
        params = {"search": tag_name}
        response = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD))
        if response.status_code == 200 and response.json():
            return response.json()[0]["id"]
        data = {"name": tag_name}
        response = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=data)
        if response.status_code == 201:
            return response.json()["id"]
        return None
    except:
        return None

def main():
    # दिन के हिसाब से 2 posts publish करें
    day_index = datetime.datetime.now().day % len(SERVICES)
    service1 = SERVICES[day_index]
    service2 = SERVICES[(day_index + 1) % len(SERVICES)]
    
    print(f"🤖 Generating blog 1: {service1['name']}")
    blog_data1 = generate_blog_post(service1["name"])
    if blog_data1:
        publish_to_wordpress(blog_data1, service1)
    
    print(f"🤖 Generating blog 2: {service2['name']}")
    blog_data2 = generate_blog_post(service2["name"])
    if blog_data2:
        publish_to_wordpress(blog_data2, service2)

if __name__ == "__main__":
    main()
