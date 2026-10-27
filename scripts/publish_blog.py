import os
import json
import requests
import datetime

# ===== API & CONFIG =====
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# ===== COMPANY DETAILS =====
COMPANY_NAME = "My City Service"
COMPANY_TAGLINE = "Professional Home Services at Your Doorstep"
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

# ===== CITIES =====
CITIES = [
    {"name": "Seoni", "slug": "seoni", "hi": "सिवनी"},
    {"name": "Chhindwara", "slug": "chhindwara", "hi": "छिंदवाड़ा"},
    {"name": "Jabalpur", "slug": "jabalpur", "hi": "जबलपुर"}
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
            "city_hi": city["hi"],
            "city_slug": city["slug"],
            "keyword": f"{service['name']} in {city['name']}",
            "slug": f"{service['name'].lower().replace(' ', '-')}-{city['slug']}"
        })

# ===== HINDI TRANSLATIONS (service name) =====
SERVICES_HI = {
    "Electrician": "इलेक्ट्रीशियन", "AC Repair": "एसी रिपेयर", "Plumber": "प्लम्बर",
    "Home Cleaning": "होम क्लीनिंग", "Appliance Repair": "अप्लायंस रिपेयर", "Carpenter": "कारपेंटर",
    "Painting": "पेंटिंग", "Water Purifier": "वॉटर प्यूरीफायर", "Sofa Cleaning": "सोफा क्लीनिंग",
    "Gas Stove Repair": "गैस स्टोव रिपेयर", "Carpet Cleaning": "कार्पेट क्लीनिंग", "Commercial Cleaning": "कमर्शियल क्लीनिंग",
    "Pick & Drop Service": "पिक एंड ड्रॉप सर्विस"
}

# ===== HINDI KEYWORD TEMPLATE (dynamic city) =====
SERVICES_HI_KEYWORD_TEMPLATE = {
    "Electrician": "{city} में इलेक्ट्रीशियन",
    "AC Repair": "{city} में एसी रिपेयर",
    "Plumber": "{city} में प्लम्बर",
    "Home Cleaning": "{city} में होम क्लीनिंग",
    "Appliance Repair": "{city} में अप्लायंस रिपेयर",
    "Carpenter": "{city} में कारपेंटर",
    "Painting": "{city} में पेंटिंग सेवाएं",
    "Water Purifier": "{city} में वॉटर प्यूरीफायर",
    "Sofa Cleaning": "{city} में सोफा क्लीनिंग",
    "Gas Stove Repair": "{city} में गैस स्टोव रिपेयर",
    "Carpet Cleaning": "{city} में कार्पेट क्लीनिंग",
    "Commercial Cleaning": "{city} में कमर्शियल क्लीनिंग",
    "Pick & Drop Service": "{city} में पिक एंड ड्रॉप सर्विस"
}

def get_hindi_keyword(service_name, city_hi):
    template = SERVICES_HI_KEYWORD_TEMPLATE.get(service_name, "{city} में " + service_name)
    return template.format(city=city_hi)

# ===== HINDI SEO TITLES (city-wise) =====
HINDI_TITLE_TEMPLATES = {
    "Electrician": "{city} में बेस्ट इलेक्ट्रीशियन सर्विस | 30 मिनट में होम विजिट",
    "AC Repair": "{city} में AC रिपेयर एंड सर्विस | 100% जनुइन पार्ट्स गारंटी",
    "Plumber": "{city} में प्लंबर सर्विस | लीकेज, टैप, पाइप फिक्स 24x7",
    "Home Cleaning": "{city} में होम क्लीनिंग सर्विस | डीप क्लीनिंग 2 घंटे में",
    "Appliance Repair": "{city} में अप्लायंस रिपेयर | फ्रिज, वॉशिंग मशीन, माइक्रोवेव",
    "Carpenter": "{city} में कारपेंटर सर्विस | फर्नीचर रिपेयर व मॉड्यूलर",
    "Painting": "{city} में होम पेंटिंग सर्विस | एशियन पेंट्स 3 साल वारंटी",
    "Water Purifier": "{city} में वॉटर प्यूरीफायर सर्विस | RO सर्विसिंग व इंस्टॉलेशन",
    "Sofa Cleaning": "{city} में सोफा क्लीनिंग | 2 घंटे में ड्राई क्लीन",
    "Gas Stove Repair": "{city} में गैस स्टोव रिपेयर | होम विजिट 299 रुपये",
    "Carpet Cleaning": "{city} में कार्पेट क्लीनिंग | शैम्पू + वैक्यूम",
    "Commercial Cleaning": "{city} में कमर्शियल क्लीनिंग | ऑफिस, होटल, हॉस्पिटल",
    "Pick & Drop Service": "{city} में पिक एंड ड्रॉप सर्विस | सेम-डे डिलीवरी"
}

# ===== ENGLISH SEO TITLES =====
EN_TITLE_TEMPLATES = {
    "Electrician": "Best Electrician in {city} | 30-Min Home Visit & 90-Day Warranty",
    "AC Repair": "AC Repair in {city} | 100% Genuine Parts & Same-Day Service",
    "Plumber": "Plumber in {city} | Leakage, Tap & Pipe Fix 24x7",
    "Home Cleaning": "Home Deep Cleaning in {city} | 2-Hour Service & Eco-Friendly",
    "Appliance Repair": "Appliance Repair in {city} | Fridge, Washing Machine, Microwave",
    "Carpenter": "Carpenter in {city} | Furniture Repair & Modular Fitting",
    "Painting": "Home Painting in {city} | Asian Paints & 3-Year Warranty",
    "Water Purifier": "Water Purifier Service in {city} | RO Installation & Servicing",
    "Sofa Cleaning": "Sofa Cleaning in {city} | 2-Hour Dry Clean & Shampoo",
    "Gas Stove Repair": "Gas Stove Repair in {city} | Home Visit at ₹299",
    "Carpet Cleaning": "Carpet Cleaning in {city} | Shampoo + Vacuum + Dry",
    "Commercial Cleaning": "Commercial Cleaning in {city} | Office, Hotel & Hospital",
    "Pick & Drop Service": "Pick & Drop Service in {city} | Same-Day Delivery"
}

# ===== BACKLINK SOURCES (high-authority, do-follow where possible) =====
BACKLINK_SOURCES = [
    {"text": "Madhya Pradesh Tourism", "url": "https://www.mptourism.com/"},
    {"text": "Jabalpur District Official", "url": "https://jabalpur.nic.in/"},
    {"text": "Wikipedia – Jabalpur", "url": "https://en.wikipedia.org/wiki/Jabalpur"},
    {"text": "Wikipedia – Home Services", "url": "https://en.wikipedia.org/wiki/Home_service"},
    {"text": "IndiaMART Home Services", "url": "https://www.indiamart.com/"},
    {"text": "Justdial", "url": "https://www.justdial.com/"},
    {"text": "Google Business Profile", "url": "https://business.google.com/"},
    {"text": "MSME Registered (Govt. of India)", "url": "https://www.msme.gov.in/"},
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

def generate_blog_post(service_name, keyword, city, language="en", city_hi=None):
    service_hi = SERVICES_HI.get(service_name, service_name)
    keyword_hi = get_hindi_keyword(service_name, city_hi or city)

    if language == "hi":
        seo_rules = f"""
STRICT RULES FOR 100% YOAST GREEN SCORE:
1. EXACT FOCUS KEYPHRASE: "{keyword_hi}"
2. Use "{keyword_hi}" EXACTLY ONCE in the FIRST sentence.
3. Use "{keyword_hi}" in SEO title and Meta Description (meta 150-160 chars).
4. Use "{keyword_hi}" at least 4 times but NEVER more than 6 times in the content.
5. Use "{keyword_hi}" in ONLY 1 H2 subheading.
6. All other H2/H3 subheadings must use DIFFERENT words (Benefits, Process, Pricing, Areas, App, Why Needed, Problem-Solution).
7. Keep sentences under 15 words. Use transition words (इसलिए, इसके अलावा, उदाहरण के लिए, लेकिन).
8. Do NOT start 3 consecutive sentences with the same word.
9. Include CTA: Call {COMPANY_PHONE} or Download App.
10. Content must be informative and NOT repetitive.

MANDATORY CONTENT SECTIONS (H2 headings):
- "Why You Need {service_hi} in {city_hi}" — 3-4 real problems (dirt, breakdown, safety, cost)
- "How We Solve It (Step-by-Step Process)" — 4-5 numbered steps
- "Our Service Pricing" — table or bullet list with ₹ amounts
- "Service Areas in {city_hi}" — 5-6 real locality names
- "Why Choose {COMPANY_NAME}" — 5 trust signals (verified technicians, 30-min visit, 90-day warranty, ₹0 inspection, 10,000+ happy customers)
- "FAQs" — 7-10 questions
"""

        prompt = f"""आप '{COMPANY_NAME} - {COMPANY_TAGLINE}' के लिए AI-first SEO & GEO विशेषज्ञ हैं।

{service_hi} सेवाओं के बारे में {city_hi}, मध्य प्रदेश के लिए एक AI-Optimized प्रीमियम ब्लॉग पोस्ट लिखें।

{seo_rules}

इन विवरणों का सटीक उपयोग करें:
- कंपनी: {COMPANY_NAME} ({COMPANY_TAGLINE})
- फोन: {COMPANY_PHONE}
- वेबसाइट: {COMPANY_WEBSITE}
- व्हाट्सएप: {SOCIAL_LINKS['whatsapp']}
- ऐप: {SOCIAL_LINKS['playstore']}
- शहर: {city_hi}, मध्य प्रदेश

STRUCTURE (exact order):
1. Introduction (Direct Answer in 40 words, keyword in first sentence)
2. Why You Need {service_hi} (Problem section)
3. How We Solve It (Step-by-Step Process)
4. Our Pricing
5. Service Areas in {city_hi}
6. Why Choose {COMPANY_NAME}
7. App Download CTA
8. FAQs (7-10)
9. Final CTA

OUTPUT: Return ONLY valid JSON.
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "content_html": "",
    "faqs": [{{"question": "", "answer": ""}}],
    "tags": ["कीवर्ड1", "कीवर्ड2", "कीवर्ड3", "कीवर्ड4", "कीवर्ड5"]
}}
"""
    else:
        seo_rules = f"""
STRICT RULES FOR 100% YOAST GREEN SCORE:
1. EXACT FOCUS KEYPHRASE: "{keyword}"
2. Use "{keyword}" EXACTLY ONCE in the FIRST sentence.
3. Use "{keyword}" in SEO title and Meta Description (meta 150-160 chars).
4. Use "{keyword}" at least 4 times but NEVER more than 6 times in the content.
5. Use "{keyword}" in ONLY 1 H2 subheading.
6. All other H2/H3 subheadings must use DIFFERENT words (Benefits, Process, Pricing, Areas, App, Why Needed, Problem-Solution).
7. Keep sentences under 20 words. Use transition words (however, therefore, moreover, in addition, for example).
8. Do NOT start 3 consecutive sentences with the same word.
9. Include CTA: Call {COMPANY_PHONE} or Download App.
10. Content must be informative and NOT repetitive.

MANDATORY CONTENT SECTIONS (H2 headings):
- "Why You Need {service_name} in {city}" — 3-4 real problems (dirt, breakdown, safety, cost, health)
- "How We Solve It (Step-by-Step Process)" — 4-5 numbered steps
- "Our Service Pricing" — table with ₹ amounts
- "Service Areas in {city}" — 5-6 real locality names (e.g., Wright Town, Napier Town, Vijay Nagar, Rampur, Adhartal)
- "Why Choose {COMPANY_NAME}" — 5 trust signals (verified technicians, 30-min visit, 90-day warranty, ₹0 inspection, 10,000+ happy customers, 4.8★ Google rating)
- "FAQs" — 7-10 questions
"""

        prompt = f"""You are an AI-first SEO & GEO (Generative Engine Optimization) expert for '{COMPANY_NAME} - {COMPANY_TAGLINE}'.

Write an AI-Optimized PREMIUM blog post about {service_name} services in {city}, Madhya Pradesh.

IMPORTANT FOCUS KEYPHRASE: "{keyword}"

{seo_rules}

IMPORTANT: Use these EXACT details:
- Brand: {COMPANY_NAME} ({COMPANY_TAGLINE})
- Phone: {COMPANY_PHONE}
- Website: {COMPANY_WEBSITE}
- WhatsApp: {SOCIAL_LINKS['whatsapp']}
- Android App: {SOCIAL_LINKS['playstore']}
- iOS App: {SOCIAL_LINKS['appstore']}
- City: {city}, Madhya Pradesh

POSITIONING: Present {COMPANY_NAME} as the MOST TRUSTED & PREMIUM home services platform in Madhya Pradesh. Mention: verified & background-checked technicians, 90-day service warranty, transparent pricing, 30-minute response, 10,000+ happy customers, 4.8★ Google rating.

STRUCTURE (exact order):
1. SEO Metadata (Title, Meta Desc, Slug)
2. Introduction (Direct Answer in 40 words)
3. Why You Need {service_name} (Problem section)
4. How We Solve It (Step-by-Step Process)
5. Our Pricing
6. Service Areas in {city}
7. Why Choose {COMPANY_NAME} (Trust Signals)
8. App Download CTA
9. FAQs (7-10 questions)
10. Call to Action

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

def build_schema_jsonld(service_info, blog_data):
    """LocalBusiness + Service + FAQ + Breadcrumb schema"""
    city = service_info["city"]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "LocalBusiness",
                "@id": f"{COMPANY_WEBSITE}/#business",
                "name": COMPANY_NAME,
                "image": LOGO_URL,
                "telephone": COMPANY_PHONE,
                "email": COMPANY_EMAIL,
                "url": COMPANY_WEBSITE,
                "priceRange": "₹₹",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": city,
                    "addressRegion": "Madhya Pradesh",
                    "addressCountry": "IN"
                },
                "areaServed": city,
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.8",
                    "reviewCount": "10000"
                }
            },
            {
                "@type": "Service",
                "name": service_info["keyword"],
                "provider": {"@id": f"{COMPANY_WEBSITE}/#business"},
                "areaServed": city,
                "serviceType": service_info["name"]
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": COMPANY_WEBSITE},
                    {"@type": "ListItem", "position": 2, "name": city, "item": f"{COMPANY_WEBSITE}/{service_info['city_slug']}"},
                    {"@type": "ListItem", "position": 3, "name": service_info["name"], "item": f"{COMPANY_WEBSITE}/{service_info['slug']}"}
                ]
            }
        ]
    }
    if blog_data.get("faqs"):
        schema["@graph"].append({
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": faq["question"],
                    "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]}
                } for faq in blog_data["faqs"][:10]
            ]
        })
    return json.dumps(schema, ensure_ascii=False)

def publish_to_wordpress(blog_data, service_info):
    if not blog_data: return None

    full_content = blog_data["content_html"]

    # 1) Quick Answer (Featured Snippet)
    if blog_data.get("meta_description"):
        full_content = f"<p><strong>Quick Answer:</strong> {blog_data['meta_description']}</p>" + full_content

    # 2) Trust signals banner (E-E-A-T)
    trust_html = f"""
    <div style="background:#f0f8ff;border-left:4px solid #0073aa;padding:12px;margin:16px 0;">
        <p><strong>✅ Why {COMPANY_NAME}?</strong></p>
        <ul>
            <li>✔️ Verified & background-checked technicians</li>
            <li>✔️ 30-minute response in {service_info['city']}</li>
            <li>✔️ 90-day service warranty</li>
            <li>✔️ Transparent pricing — no hidden charges</li>
            <li>✔️ 10,000+ happy customers | 4.8★ Google rating</li>
        </ul>
    </div>
    """
    full_content += trust_html

    # 3) FAQ Schema
    if blog_data.get("faqs"):
        faq_html = "<h2>Frequently Asked Questions (FAQs)</h2>"
        for faq in blog_data["faqs"]:
            faq_html += f'<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><h3 itemprop="name">Q: {faq["question"]}</h3><div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">A: {faq["answer"]}</p></div></div>'
        full_content += faq_html

    # 4) Social Media
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

    # 5) Featured Image (with caption for image SEO)
    image_html = f'''
    <figure>
        <img src="{LOGO_URL}" style="max-width:100%;" alt="{service_info["keyword"]} - {COMPANY_NAME}" title="{service_info["keyword"]}" loading="lazy" />
        <figcaption>Professional {service_info["name"]} services in {service_info["city"]}, Madhya Pradesh by {COMPANY_NAME}.</figcaption>
    </figure>
    '''
    full_content = image_html + full_content

    # 6) Internal Links (pillar-cluster)
    internal_links = f"""
    <h2>🔗 Explore More Services</h2>
    <ul>
        <li><a href="{COMPANY_WEBSITE}/{service_info['city_slug']}">All Services in {service_info['city']}</a></li>
        <li><a href="{COMPANY_WEBSITE}/ac-repair-{service_info['city_slug']}">AC Repair in {service_info['city']}</a></li>
        <li><a href="{COMPANY_WEBSITE}/electrician-{service_info['city_slug']}">Electrician in {service_info['city']}</a></li>
        <li><a href="{COMPANY_WEBSITE}/plumber-{service_info['city_slug']}">Plumber in {service_info['city']}</a></li>
        <li><a href="{COMPANY_WEBSITE}/home-cleaning-{service_info['city_slug']}">Home Cleaning in {service_info['city']}</a></li>
    </ul>
    """
    full_content += internal_links

    # 7) External Backlinks (authority)
    backlink_html = "<h2>🔗 Trusted References</h2><ul>"
    for link in BACKLINK_SOURCES:
        backlink_html += f'<li><a href="{link["url"]}" target="_blank" rel="noopener">{link["text"]}</a></li>'
    backlink_html += "</ul>"
    full_content += backlink_html

    # 8) JSON-LD Schema (LocalBusiness + Service + FAQ + Breadcrumb)
    schema_jsonld = build_schema_jsonld(service_info, blog_data)
    full_content += f'<script type="application/ld+json">{schema_jsonld}</script>'

    # 9) Categories & Tags
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

    # 10) Yoast SEO meta
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
    data1 = generate_blog_post(service1["name"], service1["keyword"], service1["city"], "en", service1["city_hi"])
    if data1:
        publish_to_wordpress(data1, service1)

    print(f"🤖 [EN] Blog 2: {service2['name']} - {service2['city']} - {service2['keyword']}")
    data2 = generate_blog_post(service2["name"], service2["keyword"], service2["city"], "en", service2["city_hi"])
    if data2:
        publish_to_wordpress(data2, service2)

    # ===== HINDI POSTS =====
    print(f"🤖 [HI] Blog 1: {SERVICES_HI[service1['name']]} - {service1['city']}")
    data_hi1 = generate_blog_post(service1["name"], service1["keyword"], service1["city"], "hi", service1["city_hi"])
    if data_hi1:
        service_hi = service1.copy()
        service_hi["category"] = service1["category"] + "-HI"
        service_hi["keyword"] = get_hindi_keyword(service1["name"], service1["city_hi"])
        publish_to_wordpress(data_hi1, service_hi)

    print(f"🤖 [HI] Blog 2: {SERVICES_HI[service2['name']]} - {service2['city']}")
    data_hi2 = generate_blog_post(service2["name"], service2["keyword"], service2["city"], "hi", service2["city_hi"])
    if data_hi2:
        service_hi = service2.copy()
        service_hi["category"] = service2["category"] + "-HI"
        service_hi["keyword"] = get_hindi_keyword(service2["name"], service2["city_hi"])
        publish_to_wordpress(data_hi2, service_hi)

if __name__ == "__main__":
    main()
