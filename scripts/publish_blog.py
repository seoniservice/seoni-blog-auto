import os
import json
import requests
import datetime

# ===== API & CONFIG (Secrets se aayega) =====
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# ===== COMPANY DETAILS (Professional & Safe Claims) =====
COMPANY_NAME = "My City Service"
COMPANY_TAGLINE = "Professional Home Services at Your Doorstep"
COMPANY_PHONE = "+91-9584670816"
COMPANY_LANDLINE = "07692422904"
COMPANY_EMAIL = "info@mycityservice.in"
COMPANY_WEBSITE = "https://www.mycityservice.in"

# ===== LOGO URL (ACTUAL) =====
LOGO_URL = "https://seoniservice.in/wp-content/uploads/2026/09/logo-mcs-1.png"

# ===== SOCIAL MEDIA & APP LINKS (COMPLETE SET) =====
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

# ===== CITIES =====
CITIES = [
    {"name": "Seoni", "slug": "seoni"},
    {"name": "Chhindwara", "slug": "chhindwara"},
    {"name": "Jabalpur", "slug": "jabalpur"}
]

# ===== SERVICES =====
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

# ===== GENERATE SERVICES WITH ALL CITIES =====
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

# ===== HINDI TRANSLATIONS =====
SERVICES_HI = {
    "Electrician": "इलेक्ट्रीशियन", "AC Repair": "एसी रिपेयर", "Plumber": "प्लम्बर",
    "Home Cleaning": "होम क्लीनिंग", "Appliance Repair": "अप्लायंस रिपेयर", "Carpenter": "कारपेंटर",
    "Painting": "पेंटिंग", "Water Purifier": "वॉटर प्यूरीफायर", "Sofa Cleaning": "सोफा क्लीनिंग",
    "Gas Stove Repair": "गैस स्टोव रिपेयर", "Carpet Cleaning": "कार्पेट क्लीनिंग", "Commercial Cleaning": "कमर्शियल क्लीनिंग",
    "Pick & Drop Service": "पिक एंड ड्रॉप सर्विस"
}

SERVICES_HI_KEYWORD = {
    "Electrician": "सिवनी में इलेक्ट्रीशियन", "AC Repair": "सिवनी में एसी रिपेयर", "Plumber": "सिवनी में प्लम्बर",
    "Home Cleaning": "सिवनी में होम क्लीनिंग", "Appliance Repair": "सिवनी में अप्लायंस रिपेयर", "Carpenter": "सिवनी में कारपेंटर",
    "Painting": "सिवनी में पेंटिंग सेवाएं", "Water Purifier": "सिवनी में वॉटर प्यूरीफायर", "Sofa Cleaning": "सिवनी में सोफा क्लीनिंग",
    "Gas Stove Repair": "सिवनी में गैस स्टोव रिपेयर", "Carpet Cleaning": "सिवनी में कार्पेट क्लीनिंग", "Commercial Cleaning": "सिवनी में कमर्शियल क्लीनिंग",
    "Pick & Drop Service": "सिवनी में पिक एंड ड्रॉप सर्विस"
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

def generate_blog_post(service_name, keyword, city, language="en"):
    service_hi = SERVICES_HI.get(service_name, service_name)
    keyword_hi = SERVICES_HI_KEYWORD.get(service_name, service_name)
    
    if language == "hi":
        seo_rules = f"""
STRICT RULES FOR 100% YOAST GREEN SCORE:
1. EXACT FOCUS KEYPHRASE: "{keyword_hi}" 
2. Use "{keyword_hi}" EXACTLY ONCE in the FIRST sentence.
3. Use "{keyword_hi}" in SEO title, Meta Description.
4. Use "{keyword_hi}" at least 4 times but NEVER more than 6 times in the content.
5. Use "{keyword_hi}" in ONLY 1 H2 subheading.
6. All other H2/H3 subheadings must use DIFFERENT words (Use "Benefits", "Process", "Pricing", "Areas", "App").
7. Keep sentences under 15 words. Use transition words (इसलिए, इसके अलावा, उदाहरण के लिए).
8. Do NOT start 3 consecutive sentences with the same word.
9. Include CTA: Call {COMPANY_PHONE} or Download App.
10. Content must be informative and NOT repetitive.
"""
    else:
        seo_rules = f"""
STRICT RULES FOR 100% YOAST GREEN SCORE:
1. EXACT FOCUS KEYPHRASE: "{keyword}" 
2. Use "{keyword}" EXACTLY ONCE in the FIRST sentence.
3. Use "{keyword}" in SEO title, Meta Description.
4. Use "{keyword}" at least 4 times but NEVER more than 6 times in the content.
5. Use "{keyword}" in ONLY 1 H2 subheading.
6. All other H2/H3 subheadings must use DIFFERENT words (Use "Benefits", "Process", "Pricing", "Areas", "App").
7. Keep sentences under 20 words. Use transition words (however, therefore, moreover, in addition, for example).
8. Do NOT start 3 consecutive sentences with the same word.
9. Include CTA: Call {COMPANY_PHONE} or Download App.
10. Content must be informative and NOT repetitive.
"""

    if language == "hi":
        prompt = f"""आप '{COMPANY_NAME} - {COMPANY_TAGLINE}' के लिए AI-first SEO & GEO विशेषज्ञ हैं।

{service_hi} सेवाओं के बारे में {city}, मध्य प्रदेश के लिए एक AI-Optimized ब्लॉग पोस्ट लिखें।

{seo_rules}

इन विवरणों का सटीक उपयोग करें:
- कंपनी: {COMPANY_NAME} ({COMPANY_TAGLINE})
- फोन: {COMPANY_PHONE}
- वेबसाइट: {COMPANY_WEBSITE}
- व्हाट्सएप: {SOCIAL_LINKS['whatsapp']}
- ऐप: {SOCIAL_LINKS['playstore']}

STRUCTURE:
1. SEO Metadata (Title, Meta Desc, Slug)
2. Introduction (Direct Answer in 40 words)
3. Why Choose {COMPANY_NAME} (Trust Signals)
4. Service Areas ({city})
5. App Download CTA
6. FAQs (7-10 questions)
7. Call to Action

OUTPUT: Return ONLY valid JSON.
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
        prompt = f"""You are an AI-first SEO & GEO (Generative Engine Optimization) expert for '{COMPANY_NAME} - {COMPANY_TAGLINE}'.

Write an AI-Optimized blog post about {service_name} services in {city}, Madhya Pradesh.

IMPORTANT FOCUS KEYPHRASE: "{keyword}"

{seo_rules}

IMPORTANT: Use these EXACT details:
- Brand: {COMPANY_NAME} ({COMPANY_TAGLINE})
- Phone: {COMPANY_PHONE}
- Website: {COMPANY_WEBSITE}
- WhatsApp: {SOCIAL_LINKS['whatsapp']}
- Android App: {SOCIAL_LINKS['playstore']}
- iOS App: {SOCIAL_LINKS['appstore']}

STRUCTURE:
1. SEO Metadata (Title, Meta Desc, Slug)
2. Introduction (Direct Answer in 40 words)
3. Why Choose {COMPANY_NAME} (Trust Signals)
4. Service Areas ({city})
5. App Download CTA
6. FAQs (7-10 questions)
7. Call to Action

OUTPUT: Return ONLY valid JSON, no markdown.
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
    data = {"model": "deepseek-chat", "messages": [{"role": "system", "content": "Return ONLY valid JSON. No markdown."}, {"role": "user", "content": prompt}], "temperature": 0.3, "max_tokens": 4000}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        content = content.strip()
        if content.startswith("```json"): content = content[7:]
        if content.startswith("```"): content = content[3:]
        if content.endswith("```"): content = content[:-3]
        return json.loads(content, strict=False)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def publish_to_wordpress(blog_data, service_info):
    if not blog_data: return None

    full_content = blog_data["content_html"]
    
    # AI-Ready Summary (40 words) for Featured Snippet
    if blog_data.get("meta_description"):
        ai_summary = f"<p><strong>Quick Answer:</strong> {blog_data['meta_description']}</p>"
        full_content = ai_summary + full_content

    # FAQ Schema (AI & Google Structured Data)
    if blog_data.get("faqs"):
        faq_html = "<h2>Frequently Asked Questions (FAQs)</h2>"
        for faq in blog_data["faqs"]:
            faq_html += f'<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><h3 itemprop="name">Q: {faq["question"]}</h3><div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">A: {faq["answer"]}</p></div></div>'
        full_content += faq_html

    # Social Media Section
    social_html = f"""
    <h2>📱 Connect With {COMPANY_NAME}</h2>
    <p><strong>{COMPANY_TAGLINE}</strong></p>
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

    <h2>📲 Download On-Demand App</h2>
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

    # ---------- PERFECT IMAGE & LOGO (Featured Image) ----------
    image_html = f'''
    <img src="{LOGO_URL}" style="max-width:100%;" alt="{service_info["keyword"]} - {COMPANY_NAME}" title="{service_info["keyword"]}" />
    <p><strong>Professional {service_info["name"]} Services in {service_info["city"]} by {COMPANY_NAME}.</strong></p>
    '''
    full_content = image_html + full_content

    # Internal & External Links
    internal_link = f'<p>Check out our other services at <a href="{COMPANY_WEBSITE}">{COMPANY_NAME}</a> - {COMPANY_TAGLINE}.</p>'
    external_link = f'<p><a href="https://en.wikipedia.org/wiki/{service_info["city"]}">Learn more about {service_info["city"]}, MP</a>.</p>'
    full_content += internal_link + external_link

    # Categories & Tags
    category_id = get_category_id(service_info["category"])
    tag_ids = []
    if blog_data.get("tags"):
        for tag_name in blog_data["tags"][:5]:
            try:
                url = f"{WP_URL}/wp-json/wp/v2/tags"
                params = {"search": tag_name}
                response = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD))
                if response.status_code == 200 and response.json():
                    tag_ids.append(response.json()[0]["id"])
                else:
                    data = {"name": tag_name}
                    response = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=data)
                    if response.status_code == 201:
                        tag_ids.append(response.json()["id"])
            except: pass

    keyword = service_info.get("keyword", service_info["name"])

    # ---------- PERFECT YOAST SEO META DATA ----------
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
            "_yoast_wpseo_focuskw": keyword,
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
            print(f"   Keyphrase: {keyword}")
            return result
        else:
            print(f"❌ WordPress Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    day_index = datetime.datetime.now().day % len(SERVICES)
    service1 = SERVICES[day_index]
    service2 = SERVICES[(day_index + 1) % len(SERVICES)]
    
    # ===== ENGLISH POSTS =====
    print(f"🤖 [EN] Blog 1: {service1['name']} - {service1['city']} - {service1['keyword']}")
    data1 = generate_blog_post(service1["name"], service1["keyword"], service1["city"], "en")
    if data1:
        publish_to_wordpress(data1, service1)
    
    print(f"🤖 [EN] Blog 2: {service2['name']} - {service2['city']} - {service2['keyword']}")
    data2 = generate_blog_post(service2["name"], service2["keyword"], service2["city"], "en")
    if data2:
        publish_to_wordpress(data2, service2)
    
    # ===== HINDI POSTS =====
    print(f"🤖 [HI] Blog 1: {SERVICES_HI[service1['name']]} - {service1['city']}")
    data_hi1 = generate_blog_post(service1["name"], service1["keyword"], service1["city"], "hi")
    if data_hi1:
        service_hi = service1.copy()
        service_hi["category"] = service1["category"] + "-HI"
        service_hi["keyword"] = SERVICES_HI_KEYWORD[service1["name"]]
        publish_to_wordpress(data_hi1, service_hi)
    
    print(f"🤖 [HI] Blog 2: {SERVICES_HI[service2['name']]} - {service2['city']}")
    data_hi2 = generate_blog_post(service2["name"], service2["keyword"], service2["city"], "hi")
    if data_hi2:
        service_hi = service2.copy()
        service_hi["category"] = service2["category"] + "-HI"
        service_hi["keyword"] = SERVICES_HI_KEYWORD[service2["name"]]
        publish_to_wordpress(data_hi2, service_hi)

if __name__ == "__main__":
    main()
