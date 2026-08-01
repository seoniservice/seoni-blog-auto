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

# ===== 13 SERVICES WITH KEYWORDS =====
SERVICES = [
    {"name": "Electrician", "category": "Electrician", "keyword": "Electrician Seoni"},
    {"name": "AC Repair", "category": "AC-Service", "keyword": "AC Repair Seoni"},
    {"name": "Plumber", "category": "Plumber", "keyword": "Plumber Seoni"},
    {"name": "Home Cleaning", "category": "Cleaning-Services", "keyword": "Home Cleaning Seoni"},
    {"name": "Appliance Repair", "category": "Appliance-Repair", "keyword": "Appliance Repair Seoni"},
    {"name": "Carpenter", "category": "Carpenter", "keyword": "Carpenter Seoni"},
    {"name": "Painting", "category": "Painting-Services", "keyword": "Painting Services Seoni"},
    {"name": "Water Purifier", "category": "Water-Purifier", "keyword": "Water Purifier Service Seoni"},
    {"name": "Sofa Cleaning", "category": "Sofa-Cleaning", "keyword": "Sofa Cleaning Seoni"},
    {"name": "Gas Stove Repair", "category": "Gas-Stove-Repair", "keyword": "Gas Stove Repair Seoni"},
    {"name": "Carpet Cleaning", "category": "Carpet-Cleaning", "keyword": "Carpet Cleaning Seoni"},
    {"name": "Commercial Cleaning", "category": "Commercial-Cleaning", "keyword": "Commercial Cleaning Seoni"},
    {"name": "Pick & Drop Service", "category": "Pick-Drop-Service", "keyword": "Pick and Drop Service Seoni"}
]

# ===== HINDI TRANSLATION =====
SERVICES_HI = {
    "Electrician": "इलेक्ट्रीशियन",
    "AC Repair": "एसी रिपेयर",
    "Plumber": "प्लम्बर",
    "Home Cleaning": "होम क्लीनिंग",
    "Appliance Repair": "अप्लायंस रिपेयर",
    "Carpenter": "कारपेंटर",
    "Painting": "पेंटिंग",
    "Water Purifier": "वॉटर प्यूरीफायर",
    "Sofa Cleaning": "सोफा क्लीनिंग",
    "Gas Stove Repair": "गैस स्टोव रिपेयर",
    "Carpet Cleaning": "कार्पेट क्लीनिंग",
    "Commercial Cleaning": "कमर्शियल क्लीनिंग",
    "Pick & Drop Service": "पिक एंड ड्रॉप सर्विस"
}

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

def generate_blog_post(service_name, keyword, language="en"):
    service_hi = SERVICES_HI.get(service_name, service_name)
    
    seo_rules = """
SEO RULES FOR GREEN SCORE (STRICT):
1. Keep EVERY sentence under 20 words. Break long sentences into short ones.
2. Use transition words (however, therefore, moreover, furthermore, in addition, consequently, for example) in at least 30% of sentences.
3. Include focus keyword in the FIRST sentence of the introduction.
4. Include focus keyword in at least 2 H2 subheadings.
5. Include focus keyword in SEO title (at the beginning).
6. Include focus keyword in meta description.
7. Include focus keyword at least 5-7 times in the content.
8. Use focus keyword EXACTLY as given (do not change it).
9. Add 1 image suggestion with alt text containing the keyphrase.
10. Add 1 external link to an authority site.
11. Write short paragraphs (max 2-3 sentences).
12. Use active voice throughout.
13. Include a call to action.
14. Use keyphrase in the last paragraph too.
"""
    
    if language == "hi":
        prompt = f"""आप '{COMPANY_NAME}' के लिए SEO विशेषज्ञ हैं।

{service_hi} सेवाओं के बारे में सिवनी, मध्य प्रदेश के लिए एक SEO-ऑप्टिमाइज्ड ब्लॉग पोस्ट लिखें।

{seo_rules}

इन विवरणों का सटीक उपयोग करें:
- फोन: {COMPANY_PHONE}
- वेबसाइट: {COMPANY_WEBSITE}
- व्हाट्सएप: {SOCIAL_LINKS['whatsapp']}
- ऐप: {SOCIAL_LINKS['playstore']}

Structure:
1. SEO Metadata: title, meta_description, slug
2. Introduction (with keyword in first paragraph)
3. Why Choose {COMPANY_NAME}
4. Service Overview
5. Pricing & Process
6. Local Service Areas
7. FAQs (5-7 questions)
8. Call to Action

OUTPUT: Return ONLY JSON. No extra text.
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "content_html": "",
    "faqs": [{{"question": "", "answer": ""}}],
    "tags": ["कीवर्ड1", "कीवर्ड2", "कीवर्ड3"]
}}
"""
    else:
        prompt = f"""You are an expert Senior SEO, GEO, and Local Content Strategist for '{COMPANY_NAME}'.

Write a comprehensive SEO-optimized blog post about {service_name} services in Seoni, Madhya Pradesh.

IMPORTANT FOCUS KEYWORD: {keyword}

{seo_rules}

IMPORTANT: Use these EXACT contact details:
- Phone: {COMPANY_PHONE}
- Website: {COMPANY_WEBSITE}
- WhatsApp: {SOCIAL_LINKS['whatsapp']}
- Android App: {SOCIAL_LINKS['playstore']}
- iOS App: {SOCIAL_LINKS['appstore']}

STRUCTURE:
1. SEO Metadata: title, meta_description, slug
2. Introduction (keyword in first paragraph)
3. Why Choose {COMPANY_NAME}
4. Service Overview
5. Pricing & Process
6. Local Service Areas
7. FAQs (7-10 questions)
8. Call to Action with contact details

OUTPUT FORMAT: Return valid JSON only. NO markdown, NO extra text.
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
        "messages": [{"role": "system", "content": "You are an expert SEO writer. Return ONLY valid JSON. No markdown."}, {"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 4000
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content, strict=False)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error for {service_name} ({language}): {e}")
        print(f"Raw: {content[:200] if content else 'EMPTY'}")
        return None
    except Exception as e:
        print(f"❌ DeepSeek Error for {service_name} ({language}): {e}")
        return None

def publish_to_wordpress(blog_data, service_info):
    if not blog_data:
        return None

    full_content = blog_data["content_html"]
    
    # FAQ Schema
    if blog_data.get("faqs"):
        faq_html = "<h2>Frequently Asked Questions (FAQs)</h2>"
        for faq in blog_data["faqs"]:
            faq_html += f'<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><h3 itemprop="name">Q: {faq["question"]}</h3><div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">A: {faq["answer"]}</p></div></div>'
        full_content += faq_html

    # Social Media Section
    social_html = f"""
    <h2>📱 Connect With {COMPANY_NAME}</h2>
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

    # ---- INTERNAL LINK ADD (SEO Green ke liye) ----
    internal_link = f'<p>Check out our other services at <a href="{COMPANY_WEBSITE}">{COMPANY_NAME}</a>.</p>'
    full_content += internal_link

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
            "_yoast_wpseo_focuskw": service_info["keyword"],
            "_yoast_wpseo_linkdex": "good",
            "_yoast_wpseo_content_score": "90"
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
    day_index = datetime.datetime.now().day % len(SERVICES)
    service1 = SERVICES[day_index]
    service2 = SERVICES[(day_index + 1) % len(SERVICES)]
    
    # ===== ENGLISH POSTS =====
    print(f"🤖 [EN] Generating blog 1: {service1['name']}")
    blog_data1 = generate_blog_post(service1["name"], service1["keyword"], "en")
    if blog_data1:
        publish_to_wordpress(blog_data1, service1)
    
    print(f"🤖 [EN] Generating blog 2: {service2['name']}")
    blog_data2 = generate_blog_post(service2["name"], service2["keyword"], "en")
    if blog_data2:
        publish_to_wordpress(blog_data2, service2)
    
    # ===== HINDI POSTS =====
    print(f"🤖 [HI] Generating blog 1: {SERVICES_HI[service1['name']]}")
    blog_data_hi1 = generate_blog_post(service1["name"], service1["keyword"], "hi")
    if blog_data_hi1:
        service_hi = service1.copy()
        service_hi["category"] = service1["category"] + "-HI"
        publish_to_wordpress(blog_data_hi1, service_hi)
    
    print(f"🤖 [HI] Generating blog 2: {SERVICES_HI[service2['name']]}")
    blog_data_hi2 = generate_blog_post(service2["name"], service2["keyword"], "hi")
    if blog_data_hi2:
        service_hi = service2.copy()
        service_hi["category"] = service2["category"] + "-HI"
        publish_to_wordpress(blog_data_hi2, service_hi)

if __name__ == "__main__":
    main()
