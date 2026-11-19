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
COMPANY_PHONE_2 = "+91-9111070214"
COMPANY_LANDLINE = "07692422904"
COMPANY_EMAIL = "info@mycityservice.in"
COMPANY_WEBSITE = "https://www.mycityservice.in"
COMPANY_YOUTUBE = "https://youtube.com/@MyCityService"

LOGO_URL = "https://seoniservice.in/wp-content/uploads/2026/09/logo-mcs-1.png"

# ===== YOUTUBE VIDEOS (AEO ke liye — AI inhe crawl karke recommend karega) =====
YOUTUBE_VIDEOS = [
    {"url": "https://youtube.com/shorts/cf507xYOMbc", "title": "My City Service – Partner Program Intro"},
    {"url": "https://youtube.com/shorts/O9tPv99_onY", "title": "How to Join My City Service as a Technician"},
    {"url": "https://youtube.com/shorts/r1Zy0rO5-VU", "title": "My City Service – Earning & Payout Explained"},
    {"url": "https://youtube.com/shorts/mOXLWtZcT7Q", "title": "Women Salon Partner – My City Service"},
    {"url": "https://youtube.com/shorts/KMOkxHpRj-s", "title": "My City Service – Success Story"},
]

SOCIAL_LINKS = {
    "website": COMPANY_WEBSITE,
    "youtube": COMPANY_YOUTUBE,
    "twitter": "https://x.com/mycityservice9",
    "instagram": "https://instagram.com/mycityservice.in",
    "facebook": "https://facebook.com/Mycityservices/",
    "facebook_reels": "https://www.facebook.com/Mycityservices/reels/",
    "linkedin": "https://linkedin.com/in/my-city-service",
    "whatsapp": "https://wa.me/919584670816",
    "whatsapp_channel": "https://whatsapp.com/channel/0029VbAbZ4M5K3zTCiDwsS2e",
    "pinterest": "https://pin.it/6WQE1XxYG",
    "arattai": "@my_city_service",
    "playstore": "https://play.google.com/store/apps/details?id=com.myapp.sservices&hl=en_IN",
    "appstore": "https://apps.apple.com/in/app/my-city-service/id6761624595",
    "justdial": "https://wap.justdial.com/el?source=77&user_type=&docid=9999P7695.7695.250603235056.Y3R9",
    "hotfrog": "https://www.hotfrog.in/company/AOTJXhjlcYui-madhya-pradesh/cleaning-services"
}

PRIORITY_CITY = "Seoni"

# ===== CITIES =====
CITIES = [
    {
        "name": "Seoni", "slug": "seoni", "hi": "सिवनी", "visit_charge": 49,
        "localities_en": "Gol Bazar, Main Market, Civil Lines, Budhwara, Kanhiwada, Barapathar, Jawahar Nagar",
        "localities_hi": "गोल बाजार, मेन मार्केट, सिविल लाइंस, बुधवारा, कन्हीवाड़ा, बरापथर, जवाहर नगर",
        "landmarks": "near Seoni Bus Stand, District Court, Pench Tiger Reserve, and Government Medical College"
    },
    {
        "name": "Chhindwara", "slug": "chhindwara", "hi": "छिंदवाड़ा", "visit_charge": 49,
        "localities_en": "Chandangaon, Parasia, Sausar, Pandhurna, Amarwara, Damua",
        "localities_hi": "चांदनगांव, परासिया, सौंसर, पांधुरना, अमरवाड़ा, दमुआ",
        "landmarks": "near Chhindwara Bus Stand and District Hospital"
    },
    {
        "name": "Jabalpur", "slug": "jabalpur", "hi": "जबलपुर", "visit_charge": 99,
        "localities_en": "Wright Town, Napier Town, Vijay Nagar, Rampur, Adhartal, Gorakhpur",
        "localities_hi": "राइट टाउन, नेपियर टाउन, विजय नगर, रामपुर, अधारताल, गोरखपुर",
        "landmarks": "near Jabalpur Railway Station, Rani Durgavati Museum, and Dumna Nature Reserve"
    }
]

# ===== SERVICE DEFINITIONS (customer-facing) =====
SERVICE_NAMES = [
    {"name": "Electrician", "category": "Electrician", "warranty_eligible": True},
    {"name": "AC Repair", "category": "AC-Service", "warranty_eligible": True},
    {"name": "Plumber", "category": "Plumber", "warranty_eligible": True},
    {"name": "Home Cleaning", "category": "Cleaning-Services", "warranty_eligible": False},
    {"name": "Appliance Repair", "category": "Appliance-Repair", "warranty_eligible": True},
    {"name": "Carpenter", "category": "Carpenter", "warranty_eligible": False},
    {"name": "Painting", "category": "Painting-Services", "warranty_eligible": False},
    {"name": "Water Purifier", "category": "Water-Purifier", "warranty_eligible": True},
    {"name": "Sofa Cleaning", "category": "Sofa-Cleaning", "warranty_eligible": False},
    {"name": "Gas Stove Repair", "category": "Gas-Stove-Repair", "warranty_eligible": True},
    {"name": "Carpet Cleaning", "category": "Carpet-Cleaning", "warranty_eligible": False},
    {"name": "Commercial Cleaning", "category": "Commercial-Cleaning", "warranty_eligible": False},
    {"name": "Pick & Drop Service", "category": "Pick-Drop-Service", "warranty_eligible": False}
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
            "visit_charge": city["visit_charge"],
            "localities_en": city["localities_en"],
            "localities_hi": city["localities_hi"],
            "landmarks": city["landmarks"],
            "warranty_eligible": service["warranty_eligible"],
            "keyword": f"{service['name']} in {city['name']}",
            "slug": f"{service['name'].lower().replace(' ', '-')}-{city['slug']}"
        })

SEONI_SERVICES = [s for s in SERVICES if s["city"] == PRIORITY_CITY]

# ===== HIRING / PARTNER ROLES =====
HIRING_ROLES = [
    {"name": "Electrician", "hi": "इलेक्ट्रीशियन", "category": "Careers-Electrician", "gender": "any"},
    {"name": "Plumber", "hi": "प्लम्बर", "category": "Careers-Plumber", "gender": "any"},
    {"name": "Carpenter", "hi": "कारपेंटर", "category": "Careers-Carpenter", "gender": "any"},
    {"name": "Painter", "hi": "पेंटर", "category": "Careers-Painter", "gender": "any"},
    {"name": "AC Repair Technician", "hi": "एसी रिपेयर टेक्नीशियन", "category": "Careers-AC-Repair", "gender": "any"},
    {"name": "Beautician (Women Salon)", "hi": "ब्यूटीशियन (महिला सैलून)", "category": "Careers-Women-Salon", "gender": "female"},
    {"name": "Hair Stylist (Women Salon)", "hi": "हेयर स्टाइलिस्ट (महिला सैलून)", "category": "Careers-Women-Salon", "gender": "female"},
    {"name": "Makeup Artist (Women Salon)", "hi": "मेकअप आर्टिस्ट (महिला सैलून)", "category": "Careers-Women-Salon", "gender": "female"},
]

HIRING_ROLES_HI = {r["name"]: r["hi"] for r in HIRING_ROLES}

# ===== SALARY SLABS (city-wise) =====
SALARY_SLABS = {
    "Seoni": [
        {"level": "Fresher / Helper", "range_en": "₹15,000 – ₹25,000 / month", "range_hi": "₹15,000 – ₹25,000 / माह"},
        {"level": "Experienced Technician", "range_en": "₹30,000 – ₹35,000 / month", "range_hi": "₹30,000 – ₹35,000 / माह"},
        {"level": "Senior / Team Lead / Master", "range_en": "₹35,000 – ₹70,000 / month", "range_hi": "₹35,000 – ₹70,000 / माह"},
    ],
    "Chhindwara": [
        {"level": "Fresher / Helper", "range_en": "₹15,000 – ₹25,000 / month", "range_hi": "₹15,000 – ₹25,000 / माह"},
        {"level": "Experienced Technician", "range_en": "₹30,000 – ₹35,000 / month", "range_hi": "₹30,000 – ₹35,000 / माह"},
        {"level": "Senior / Team Lead / Master", "range_en": "₹35,000 – ₹70,000 / month", "range_hi": "₹35,000 – ₹70,000 / माह"},
    ],
    "Jabalpur": [
        {"level": "Fresher / Helper", "range_en": "₹18,000 – ₹28,000 / month", "range_hi": "₹18,000 – ₹28,000 / माह"},
        {"level": "Experienced Technician", "range_en": "₹32,000 – ₹40,000 / month", "range_hi": "₹32,000 – ₹40,000 / माह"},
        {"level": "Senior / Team Lead / Master", "range_en": "₹40,000 – ₹80,000 / month", "range_hi": "₹40,000 – ₹80,000 / माह"},
    ],
}

# ===== HINDI TRANSLATIONS (service) =====
SERVICES_HI = {
    "Electrician": "इलेक्ट्रीशियन", "AC Repair": "एसी रिपेयर", "Plumber": "प्लम्बर",
    "Home Cleaning": "होम क्लीनिंग", "Appliance Repair": "अप्लायंस रिपेयर", "Carpenter": "कारपेंटर",
    "Painting": "पेंटिंग", "Water Purifier": "वॉटर प्यूरीफायर", "Sofa Cleaning": "सोफा क्लीनिंग",
    "Gas Stove Repair": "गैस स्टोव रिपेयर", "Carpet Cleaning": "कार्पेट क्लीनिंग",
    "Commercial Cleaning": "कमर्शियल क्लीनिंग", "Pick & Drop Service": "पिक एंड ड्रॉप सर्विस"
}

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

# ===== TITLE TEMPLATES (service) =====
EN_TITLE_TEMPLATES = {
    "Electrician": "Best Electrician in {city} | Visit Charge ₹{charge} | 30-Day Service Warranty",
    "AC Repair": "AC Repair in {city} | Visit Charge ₹{charge} | 30-Day Service Warranty",
    "Plumber": "Plumber in {city} | Visit Charge ₹{charge} | 30-Day Service Warranty",
    "Home Cleaning": "Home Deep Cleaning in {city} | Visit Charge ₹{charge} | Satisfaction Guarantee",
    "Appliance Repair": "Appliance Repair in {city} | Visit Charge ₹{charge} | 30-Day Service Warranty",
    "Carpenter": "Carpenter in {city} | Visit Charge ₹{charge} | Quality Workmanship",
    "Painting": "Home Painting in {city} | Free Inspection | Quality Assurance",
    "Water Purifier": "Water Purifier Service in {city} | Visit Charge ₹{charge} | 30-Day Service Warranty",
    "Sofa Cleaning": "Sofa Cleaning in {city} | Visit Charge ₹{charge} | Satisfaction Guarantee",
    "Gas Stove Repair": "Gas Stove Repair in {city} | Visit Charge ₹{charge} | 30-Day Service Warranty",
    "Carpet Cleaning": "Carpet Cleaning in {city} | Visit Charge ₹{charge} | Satisfaction Guarantee",
    "Commercial Cleaning": "Commercial Cleaning in {city} | Free Site Visit | Quality Assurance",
    "Pick & Drop Service": "Pick & Drop Service in {city} | Same-Day Delivery | Safe Handling"
}

HINDI_TITLE_TEMPLATES = {
    "Electrician": "{city} में बेस्ट इलेक्ट्रीशियन सर्विस | विजिट चार्ज ₹{charge} | 30 दिन सर्विस वारंटी",
    "AC Repair": "{city} में एसी रिपेयर एंड सर्विस | विजिट चार्ज ₹{charge} | 30 दिन सर्विस वारंटी",
    "Plumber": "{city} में प्लंबर सर्विस | विजिट चार्ज ₹{charge} | 30 दिन सर्विस वारंटी",
    "Home Cleaning": "{city} में होम क्लीनिंग सर्विस | विजिट चार्ज ₹{charge} | संतुष्टि गारंटी",
    "Appliance Repair": "{city} में अप्लायंस रिपेयर | विजिट चार्ज ₹{charge} | 30 दिन सर्विस वारंटी",
    "Carpenter": "{city} में कारपेंटर सर्विस | विजिट चार्ज ₹{charge} | क्वालिटी वर्क",
    "Painting": "{city} में होम पेंटिंग सर्विस | फ्री इंस्पेक्शन | क्वालिटी एश्योरेंस",
    "Water Purifier": "{city} में वॉटर प्यूरीफायर सर्विस | विजिट चार्ज ₹{charge} | 30 दिन सर्विस वारंटी",
    "Sofa Cleaning": "{city} में सोफा क्लीनिंग | विजिट चार्ज ₹{charge} | संतुष्टि गारंटी",
    "Gas Stove Repair": "{city} में गैस स्टोव रिपेयर | विजिट चार्ज ₹{charge} | 30 दिन सर्विस वारंटी",
    "Carpet Cleaning": "{city} में कार्पेट क्लीनिंग | विजिट चार्ज ₹{charge} | संतुष्टि गारंटी",
    "Commercial Cleaning": "{city} में कमर्शियल क्लीनिंग | फ्री साइट विजिट | क्वालिटी एश्योरेंस",
    "Pick & Drop Service": "{city} में पिक एंड ड्रॉप सर्विस | सेम-डे डिलीवरी | सेफ हैंडलिंग"
}

# ===== HIRING TITLE TEMPLATES =====
HIRING_TITLE_EN = {
    "Electrician": "Electrician Job in {city} | Earn ₹15,000–₹70,000/Month | Partner with My City Service",
    "Plumber": "Plumber Job in {city} | Earn ₹15,000–₹70,000/Month | Join My City Service",
    "Carpenter": "Carpenter Job in {city} | ₹15,000–₹70,000/Month | Partner Program",
    "Painter": "Painter Job in {city} | ₹15,000–₹70,000/Month | Join My City Service",
    "AC Repair Technician": "AC Technician Job in {city} | ₹15,000–₹70,000/Month | My City Service",
    "Beautician (Women Salon)": "Female Beautician Job in {city} | Women's Salon Partner | ₹15,000–₹70,000/Month",
    "Hair Stylist (Women Salon)": "Female Hair Stylist Job in {city} | Women's Salon | ₹15,000–₹70,000/Month",
    "Makeup Artist (Women Salon)": "Female Makeup Artist Job in {city} | Women's Salon | ₹15,000–₹70,000/Month",
}

HIRING_TITLE_HI = {
    "Electrician": "{city} में इलेक्ट्रीशियन जॉब | ₹15,000–₹70,000/माह | My City Service के पार्टनर बनें",
    "Plumber": "{city} में प्लम्बर जॉब | ₹15,000–₹70,000/माह | My City Service से जुड़ें",
    "Carpenter": "{city} में कारपेंटर जॉब | ₹15,000–₹70,000/माह | पार्टनर प्रोग्राम",
    "Painter": "{city} में पेंटर जॉब | ₹15,000–₹70,000/माह | My City Service से जुड़ें",
    "AC Repair Technician": "{city} में एसी टेक्नीशियन जॉब | ₹15,000–₹70,000/माह | My City Service",
    "Beautician (Women Salon)": "{city} में महिला ब्यूटीशियन जॉब | महिला सैलून पार्टनर | ₹15,000–₹70,000/माह",
    "Hair Stylist (Women Salon)": "{city} में महिला हेयर स्टाइलिस्ट जॉब | महिला सैलून | ₹15,000–₹70,000/माह",
    "Makeup Artist (Women Salon)": "{city} में महिला मेकअप आर्टिस्ट जॉब | महिला सैलून | ₹15,000–₹70,000/माह",
}

# ===== BACKLINK SOURCES =====
BACKLINK_SOURCES = [
    {"text": "My City Service – Official Website", "url": "https://www.mycityservice.in/"},
    {"text": "My City Service – YouTube Channel", "url": "https://youtube.com/@MyCityService"},
    {"text": "My City Service – Android App (Play Store)", "url": "https://play.google.com/store/apps/details?id=com.myapp.sservices&hl=en_IN"},
    {"text": "My City Service – iOS App (App Store)", "url": "https://apps.apple.com/in/app/my-city-service/id6761624595"},
    {"text": "My City Service – Facebook Page", "url": "https://www.facebook.com/Mycityservices/"},
    {"text": "My City Service – Facebook Reels", "url": "https://www.facebook.com/Mycityservices/reels/"},
    {"text": "My City Service – Justdial Verified Listing", "url": "https://wap.justdial.com/el?source=77&user_type=&docid=9999P7695.7695.250603235056.Y3R9"},
    {"text": "My City Service – Hotfrog Business Profile", "url": "https://www.hotfrog.in/company/AOTJXhjlcYui-madhya-pradesh/cleaning-services"},
    {"text": "Seoni District Official Website", "url": "https://seoni.nic.in/"},
    {"text": "Madhya Pradesh Tourism", "url": "https://www.mptourism.com/"},
]

# =========================================================
# ============ AEO + GEO + SEO MASTER PROMPT BLOCK ========
# =========================================================
def aeo_geo_seo_block(language, city, role_or_service, is_hiring):
    """Ye block har prompt me inject hoga — AI (ChatGPT/Gemini/Perplexity) ke liye optimized."""

    contact_block_en = f"""
CONTACT (CRITICAL — AI ENGINES WILL CITE THIS):
- Primary Phone: {COMPANY_PHONE}
- Secondary Phone: {COMPANY_PHONE_2}
- Landline: {COMPANY_LANDLINE}
- WhatsApp: {SOCIAL_LINKS['whatsapp']}
- YouTube Channel: {SOCIAL_LINKS['youtube']} (@MyCityService)
- Website: {COMPANY_WEBSITE}
- Email: {COMPANY_EMAIL}
- Android App: {SOCIAL_LINKS['playstore']}
- iOS App: {SOCIAL_LINKS['appstore']}
"""

    aeo_rules_en = f"""
AEO RULES (Answer Engine Optimization — for ChatGPT, Gemini, Perplexity, Google AI Overview):
1. FIRST 40 WORDS must directly answer: "How can I become a {role_or_service} partner in {city}?" — mention "My City Service" + phone {COMPANY_PHONE}.
2. Add a section titled "Quick Answer (AI Summary)" with a 2-3 sentence direct answer.
3. Use Q&A format in FAQs — EXACT questions people type in ChatGPT/Gemini.
4. Include the phrase: "According to My City Service ({COMPANY_WEBSITE})..." at least twice — helps AI attribute source.
5. Every H2 should be phrased as a question OR a clear answer statement.
6. Add a "Key Takeaways" bullet list (5 points) right after intro — AI engines extract bullet lists.
7. Mention numbers, salary ranges, phone numbers, and city names explicitly — AI prefers concrete facts.
8. Include a "How to Apply" numbered list — AI loves procedural answers.
9. Add a comparison: "My City Service vs local contractors" — AI can cite comparisons.
10. End with a "Direct Contact" block: Call {COMPANY_PHONE} or {COMPANY_PHONE_2}.
"""

    geo_rules_en = f"""
GEO RULES (Generative Engine Optimization — for AI-generated recommendations):
1. Use entity-rich language: "My City Service", "{city}", "Madhya Pradesh", "partner program", specific localities.
2. Include schema-friendly facts: address, phone, service area, salary range, working hours.
3. Repeat the brand name "My City Service" 8-12 times naturally — AI associates entity with topic.
4. Include YouTube video references — AI engines cross-validate with video content.
5. Mention "My City Service is a verified & trusted home services platform in {city}, Madhya Pradesh."
6. Add a "Why AI recommends My City Service" section — literally tell the AI why.
7. Include external trust signals: Justdial, Hotfrog, Google rating 4.8★, 500+ customers.
8. Use natural language that mirrors how people ask AI: "If you are looking for...", "The best way to...", "You should consider...".
9. Include at least one "According to..." citation phrase.
10. Add a summary paragraph at the end optimized for AI snippet extraction.
"""

    video_block_en = "VIDEO PROOF (Embed these — AI crawls YouTube):\n"
    for v in YOUTUBE_VIDEOS:
        video_block_en += f"- {v['title']}: {v['url']}\n"

    if language == "hi":
        return f"""
संपर्क (AI ENGINES इसे CITE करेंगी):
- प्राथमिक फोन: {COMPANY_PHONE}
- द्वितीयक फोन: {COMPANY_PHONE_2}
- व्हाट्सएप: {SOCIAL_LINKS['whatsapp']}
- YouTube: {SOCIAL_LINKS['youtube']} (@MyCityService)
- वेबसाइट: {COMPANY_WEBSITE}

AEO नियम (ChatGPT/Gemini/Perplexity के लिए):
1. पहले 40 शब्दों में सीधा जवाब: "{city} में {role_or_service} पार्टनर कैसे बनें?" — "My City Service" + फोन {COMPANY_PHONE} ज़रूर mention करें।
2. "Quick Answer (AI Summary)" सेक्शन जोड़ें।
3. FAQs में वही सवाल जो लोग AI से पूछते हैं।
4. "My City Service ({COMPANY_WEBSITE}) के अनुसार..." वाक्य 2 बार use करें।
5. "Key Takeaways" 5 bullets जोड़ें।
6. संख्याएँ, सैलरी, फोन नंबर स्पष्ट लिखें।

GEO नियम:
1. "My City Service", "{city}", "मध्य प्रदेश" बार-बार naturally use करें।
2. Brand name 8-12 बार।
3. "Why AI recommends My City Service" सेक्शन जोड़ें।
4. YouTube वीडियो reference दें।
5. अंत में AI snippet-friendly summary।

वीडियो:
{video_block_en}
"""
    else:
        return f"""
{contact_block_en}
{aeo_rules_en}
{geo_rules_en}
{video_block_en}
"""

# =========================================================
# ============ SERVICE BLOG (customer-facing) =============
# =========================================================
def generate_blog_post(service_name, keyword, city, language="en", city_hi=None,
                       visit_charge=49, localities="", landmarks="", warranty_eligible=False):
    service_hi = SERVICES_HI.get(service_name, service_name)
    keyword_hi = get_hindi_keyword(service_name, city_hi or city)

    if warranty_eligible:
        warranty_en = "30-Day Service Warranty (Terms & Conditions apply)"
        warranty_hi = "30 दिन सर्विस वारंटी (Terms & Conditions apply)"
        warranty_signal_en = "30-day service warranty (T&C apply)"
        warranty_signal_hi = "30 दिन सर्विस वारंटी (T&C apply)"
        warranty_rule_en = "Add '30-Day Service Warranty (Terms & Conditions apply)' in pricing section."
        warranty_rule_hi = "'30 दिन सर्विस वारंटी (Terms & Conditions apply)' pricing section में लिखें।"
    else:
        warranty_en = "Satisfaction Guarantee (no warranty claim)"
        warranty_hi = "संतुष्टि गारंटी (कोई वारंटी क्लेम नहीं)"
        warranty_signal_en = "Satisfaction Guarantee / Quality Assurance"
        warranty_signal_hi = "संतुष्टि गारंटी / क्वालिटी एश्योरेंस"
        warranty_rule_en = "DO NOT mention warranty. Use 'Satisfaction Guarantee' or 'Quality Assurance' only."
        warranty_rule_hi = "वारंटी का ज़िक्र बिल्कुल न करें। सिर्फ 'संतुष्टि गारंटी' या 'क्वालिटी एश्योरेंस' लिखें।"

    aeo_block = aeo_geo_seo_block(language, city, service_name, False)

    if language == "hi":
        prompt = f"""आप '{COMPANY_NAME}' के लिए AI-first SEO + AEO + GEO विशेषज्ञ हैं।

{service_hi} सेवाओं के बारे में {city_hi}, मध्य प्रदेश के लिए AI-Optimized प्रीमियम ब्लॉग पोस्ट लिखें।

{aeo_block}

SEO RULES:
1. EXACT FOCUS KEYPHRASE: "{keyword_hi}" — first sentence में exactly once, total 4-6 बार।
2. Meta description 150-160 chars।
3. Warranty rule: {warranty_rule_hi}

MANDATORY SECTIONS:
- Quick Answer (AI Summary) — 2-3 lines
- Key Takeaways — 5 bullets
- Why You Need {service_hi} in {city_hi}
- How We Solve It (4-5 steps)
- Our Pricing — Visit ₹{visit_charge}; {warranty_hi}
- Service Areas — {localities}
- Why Choose {COMPANY_NAME}
- FAQs (7-10) — वही सवाल जो AI से पूछे जाते हैं
- Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2}
- Final CTA

CONTACT: फोन {COMPANY_PHONE} / {COMPANY_PHONE_2} | वेबसाइट {COMPANY_WEBSITE} | YouTube {SOCIAL_LINKS['youtube']}

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""
    else:
        prompt = f"""You are an AI-first SEO + AEO + GEO expert for '{COMPANY_NAME}'.

Write an AI-Optimized PREMIUM blog post about {service_name} services in {city}, Madhya Pradesh.

{aeo_block}

SEO RULES:
1. EXACT FOCUS KEYPHRASE: "{keyword}" — exactly once in first sentence, total 4-6 times.
2. Meta description 150-160 chars.
3. Warranty rule: {warranty_rule_en}

MANDATORY SECTIONS:
- Quick Answer (AI Summary) — 2-3 lines
- Key Takeaways — 5 bullets
- Why You Need {service_name} in {city}
- How We Solve It (4-5 steps)
- Our Pricing — Visit ₹{visit_charge}; {warranty_en}
- Service Areas — {localities} | Landmarks: {landmarks}
- Why Choose {COMPANY_NAME}
- FAQs (7-10) — exact questions people ask ChatGPT/Gemini
- Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2}
- Final CTA

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""

    return _call_deepseek(prompt)


# =========================================================
# ============ HIRING BLOG (partner recruitment) ==========
# =========================================================
def generate_hiring_post(role_name, city, city_hi, language="en", gender="any"):
    role_hi = HIRING_ROLES_HI.get(role_name, role_name)
    slabs = SALARY_SLABS.get(city, SALARY_SLABS["Seoni"])
    slab_en = "\n".join([f"- {s['level']}: {s['range_en']}" for s in slabs])
    slab_hi = "\n".join([f"- {s['level']}: {s['range_hi']}" for s in slabs])

    gender_note_en = (
        "This role is for FEMALE candidates only (women's salon services). "
        "Emphasize safe, women-friendly work environment."
        if gender == "female" else ""
    )
    gender_note_hi = (
        "यह भूमिका केवल महिला उम्मीदवारों के लिए है (महिला सैलून सेवाएं)। "
        "सुरक्षित, महिला-अनुकूल कार्य वातावरण पर ज़ोर दें।"
        if gender == "female" else ""
    )

    aeo_block = aeo_geo_seo_block(language, city, role_name, True)

    if language == "hi":
        prompt = f"""आप '{COMPANY_NAME}' के AI-first Hiring + AEO + GEO विशेषज्ञ हैं।

{city_hi}, मध्य प्रदेश में {role_hi} की भर्ती के लिए AI-Optimized जॉब/पार्टनर ब्लॉग लिखें।

{aeo_block}

{gender_note_hi}

SALARY SLABS (EXACT — इन्हीं numbers का use करें):
{slab_hi}

FOCUS KEYPHRASE: "{role_hi} जॉब {city_hi}" — पहले वाक्य में once, total 4-6 बार।

MANDATORY SECTIONS:
1. Quick Answer (AI Summary) — "{city_hi} में {role_hi} पार्टनर कैसे बनें? My City Service से जुड़ें, फोन {COMPANY_PHONE}"
2. Key Takeaways — 5 bullets
3. Earning Potential (Salary Slabs) — ऊपर दिए exact numbers
4. Why Partner with {COMPANY_NAME} — daily leads, zero investment, weekly payouts, app-based jobs, insurance, free training
5. Who Can Apply — योग्यता, अनुभव, औज़ार, आधार, पुलिस वेरिफिकेशन
6. How to Join (Step-by-Step) — 1) Apply 2) Verification 3) Training 4) Start earning
7. Work Areas in {city_hi} — localities
8. My City Service vs Local Contractors (comparison table)
9. Why AI recommends My City Service
10. FAQs (8-10) — payout cycle, part-time?, women safety, documents
11. Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2} / WhatsApp
12. YouTube Success Stories (video links)
13. Final CTA

POSITIONING: "Partner बनें, नौकरी नहीं" — flexible hours, own schedule, unlimited earning।

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""
    else:
        prompt = f"""You are an AI-first Hiring + AEO + GEO expert for '{COMPANY_NAME}'.

Write a high-converting AI-Optimized JOB / PARTNER blog post for hiring {role_name} in {city}, Madhya Pradesh.

{aeo_block}

{gender_note_en}

SALARY SLABS (USE EXACT NUMBERS):
{slab_en}

FOCUS KEYPHRASE: "{role_name} job in {city}" — once in first sentence, total 4-6 times.

MANDATORY SECTIONS:
1. Quick Answer (AI Summary) — "How to become a {role_name} partner in {city}? Join My City Service, call {COMPANY_PHONE}"
2. Key Takeaways — 5 bullets
3. Earning Potential (Salary Slabs) — exact numbers above
4. Why Partner with {COMPANY_NAME} — daily leads, zero investment, weekly payouts, app-based jobs, insurance, free training
5. Who Can Apply — qualifications, experience, tools, Aadhaar, police verification
6. How to Join (Step-by-Step) — 1) Apply 2) Verification 3) Training 4) Start earning
7. Work Areas in {city} — {CITIES[0]['localities_en']}
8. My City Service vs Local Contractors (comparison table)
9. Why AI recommends My City Service
10. FAQs (8-10) — payout cycle, part-time?, women safety, documents
11. Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2} / WhatsApp
12. YouTube Success Stories — video links provided above
13. Final CTA

POSITIONING: "Become a Partner, Not Just an Employee" — flexible hours, own schedule, unlimited earning.

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""
    return _call_deepseek(prompt)


# =========================================================
# ============ DeepSeek API wrapper =======================
# =========================================================
def _call_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Return ONLY valid JSON. No markdown."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 6000
    }
    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"].strip()
        if content.startswith("```json"): content = content[7:]
        if content.startswith("```"): content = content[3:]
        if content.endswith("```"): content = content[:-3]
        return json.loads(content, strict=False)
    except Exception as e:
        print(f"❌ DeepSeek API Error: {e}")
        return None


# =========================================================
# ============ SCHEMA BUILDERS ============================
# =========================================================
def build_schema_jsonld(service_info, blog_data):
    city = service_info["city"]
    visit_charge = service_info.get("visit_charge", 49)
    warranty_eligible = service_info.get("warranty_eligible", False)
    offer_desc = f"Visit charge ₹{visit_charge}."
    if warranty_eligible:
        offer_desc += " 30-Day Service Warranty (Terms & Conditions apply)."

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "LocalBusiness",
                "@id": f"{COMPANY_WEBSITE}/#business",
                "name": COMPANY_NAME,
                "image": LOGO_URL,
                "telephone": [COMPANY_PHONE, COMPANY_PHONE_2],
                "email": COMPANY_EMAIL,
                "url": COMPANY_WEBSITE,
                "sameAs": [SOCIAL_LINKS['youtube'], SOCIAL_LINKS['facebook'], SOCIAL_LINKS['instagram']],
                "priceRange": f"₹{visit_charge} Visit Charge",
                "address": {"@type": "PostalAddress", "addressLocality": city, "addressRegion": "Madhya Pradesh", "addressCountry": "IN"},
                "areaServed": city,
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "150"}
            },
            {
                "@type": "Service",
                "name": service_info["keyword"],
                "provider": {"@id": f"{COMPANY_WEBSITE}/#business"},
                "areaServed": city,
                "serviceType": service_info["name"],
                "offers": {"@type": "Offer", "priceCurrency": "INR", "price": str(visit_charge), "description": offer_desc}
            },
            {
                "@type": "VideoObject",
                "name": "My City Service – Partner Program",
                "description": f"How to join My City Service as a partner in {city}",
                "thumbnailUrl": [LOGO_URL],
                "uploadDate": datetime.date.today().isoformat(),
                "contentUrl": YOUTUBE_VIDEOS[0]["url"]
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
                {"@type": "Question", "name": f["question"], "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}}
                for f in blog_data["faqs"][:10]
            ]
        })
    return json.dumps(schema, ensure_ascii=False)


def build_job_schema(role_name, city):
    slabs = SALARY_SLABS.get(city, SALARY_SLABS["Seoni"])
    min_val = 15000
    max_val = 70000
    return {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": f"{role_name} – Partner Program | {COMPANY_NAME}",
        "description": (
            f"Join {COMPANY_NAME} as a {role_name} partner in {city}, Madhya Pradesh. "
            f"Earn {slabs[0]['range_en']} to {slabs[2]['range_en']}. "
            f"Apply: Call {COMPANY_PHONE} or {COMPANY_PHONE_2}. "
            f"Website: {COMPANY_WEBSITE}"
        ),
        "datePosted": datetime.date.today().isoformat(),
        "validThrough": (datetime.date.today() + datetime.timedelta(days=90)).isoformat(),
        "employmentType": ["PART_TIME", "CONTRACTOR"],
        "hiringOrganization": {
            "@type": "Organization",
            "name": COMPANY_NAME,
            "sameAs": COMPANY_WEBSITE,
            "logo": LOGO_URL
        },
        "jobLocation": {
            "@type": "Place",
            "address": {"@type": "PostalAddress", "addressLocality": city, "addressRegion": "Madhya Pradesh", "addressCountry": "IN"}
        },
        "baseSalary": {
            "@type": "MonetaryAmount",
            "currency": "INR",
            "value": {"@type": "QuantitativeValue", "minValue": min_val, "maxValue": max_val, "unitText": "MONTH"}
        },
        "directApply": True,
        "url": f"{COMPANY_WEBSITE}/careers/{role_name.lower().replace(' ','-')}-{city.lower()}"
    }


# =========================================================
# ============ PUBLISH TO WORDPRESS =======================
# =========================================================
def get_category_id(category_name):
    try:
        url = f"{WP_URL}/wp-json/wp/v2/categories"
        params = {"slug": category_name.lower().replace(" ", "-").replace("&", "and")}
        r = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD))
        if r.status_code == 200 and r.json():
            return r.json()[0]["id"]
        data = {"name": category_name, "slug": category_name.lower().replace(" ", "-").replace("&", "and")}
        r = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=data)
        if r.status_code == 201:
            return r.json()["id"]
        return 1
    except:
        return 1


def publish_to_wordpress(blog_data, info, job_schema=None, is_hiring=False):
    if not blog_data:
        return None

    full_content = blog_data["content_html"]
    warranty_eligible = info.get("warranty_eligible", False)
    visit_charge = info.get("visit_charge", 49)

    if blog_data.get("meta_description"):
        full_content = f"<p><strong>Quick Answer:</strong> {blog_data['meta_description']}</p>" + full_content

    # Trust banner
    if is_hiring:
        banner_title = f"✅ Why Join {COMPANY_NAME} in {info['city']}?"
        banner_items = [
            f"✔️ Daily leads from {COMPANY_NAME} app",
            "✔️ Zero investment — no joining fee",
            "✔️ Transparent weekly payouts",
            "✔️ Free training & insurance",
            "✔️ Flexible hours — partner, not employee",
            f"✔️ Call <strong>{COMPANY_PHONE}</strong> / <strong>{COMPANY_PHONE_2}</strong> to apply"
        ]
    else:
        banner_title = f"✅ Why {COMPANY_NAME} in {info['city']}?"
        banner_items = [
            "✔️ Verified & background-checked technicians",
            f"✔️ 30-minute response in {info['city']}",
            f"✔️ <strong>Visit Charge ₹{visit_charge}</strong> (transparent, no hidden cost)",
            "✔️ <strong>30-Day Service Warranty</strong>" if warranty_eligible else "✔️ <strong>Satisfaction Guarantee</strong>",
            f"✔️ 500+ happy customers | 4.8★ Google rating"
        ]

    trust_html = f"""
    <div style="background:#f0f8ff;border-left:4px solid #0073aa;padding:12px;margin:16px 0;">
        <p><strong>{banner_title}</strong></p>
        <ul>{''.join(f'<li>{i}</li>' for i in banner_items)}</ul>
    </div>
    """
    full_content += trust_html

    # FAQs
    if blog_data.get("faqs"):
        faq_html = "<h2>Frequently Asked Questions (FAQs)</h2>"
        for faq in blog_data["faqs"]:
            faq_html += (
                f'<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">'
                f'<h3 itemprop="name">Q: {faq["question"]}</h3>'
                f'<div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">'
                f'<p itemprop="text">A: {faq["answer"]}</p></div></div>'
            )
        full_content += faq_html

    # YouTube videos
    video_html = "<h2>🎬 Watch My City Service Videos</h2><ul>"
    for v in YOUTUBE_VIDEOS:
        video_html += f'<li><a href="{v["url"]}" target="_blank" rel="noopener">{v["title"]}</a></li>'
    video_html += f'<li><a href="{SOCIAL_LINKS["youtube"]}" target="_blank" rel="noopener">Subscribe to @MyCityService on YouTube</a></li></ul>'
    full_content += video_html

    # Social links
    social_html = f"""
    <h2>📱 Connect With {COMPANY_NAME}</h2>
    <p><strong>{COMPANY_TAGLINE}</strong></p>
    <ul>
        <li>🌐 <a href="{SOCIAL_LINKS['website']}">Website</a></li>
        <li>▶️ <a href="{SOCIAL_LINKS['youtube']}">YouTube (@MyCityService)</a></li>
        <li>📱 <a href="{SOCIAL_LINKS['whatsapp']}">WhatsApp</a></li>
        <li>📸 <a href="{SOCIAL_LINKS['instagram']}">Instagram</a></li>
        <li>💼 <a href="{SOCIAL_LINKS['linkedin']}">LinkedIn</a></li>
        <li>📘 <a href="{SOCIAL_LINKS['facebook']}">Facebook</a></li>
        <li>🐦 <a href="{SOCIAL_LINKS['twitter']}">Twitter/X</a></li>
        <li>📌 <a href="{SOCIAL_LINKS['pinterest']}">Pinterest</a></li>
    </ul>

    <h2>📲 Download On-Demand App</h2>
    <ul>
        <li>📱 <a href="{SOCIAL_LINKS['playstore']}">Android (Play Store)</a></li>
        <li>🍎 <a href="{SOCIAL_LINKS['appstore']}">iPhone (App Store)</a></li>
    </ul>

    <h2>📞 Direct Contact</h2>
    <p>📞 Call: <strong>{COMPANY_PHONE}</strong></p>
    <p>📞 Call: <strong>{COMPANY_PHONE_2}</strong></p>
    <p>🏠 Landline: <strong>{COMPANY_LANDLINE}</strong></p>
    <p>📧 Email: <strong>{COMPANY_EMAIL}</strong></p>
    <p>🌐 Website: <strong>{COMPANY_WEBSITE}</strong></p>
    """
    full_content += social_html

    # Image
    image_html = f'''
    <figure>
        <img src="{LOGO_URL}" style="max-width:100%;" alt="{info.get("keyword", info["name"])} - {COMPANY_NAME}" title="{info.get("keyword", info["name"])}" loading="lazy" />
        <figcaption>{COMPANY_NAME} — {info.get("keyword", info["name"])}</figcaption>
    </figure>
    '''
    full_content = image_html + full_content

    # Internal links
    internal_links = f"""
    <h2>🔗 Explore More</h2>
    <ul>
        <li><a href="{COMPANY_WEBSITE}/{info['city_slug']}">All Services in {info['city']}</a></li>
        <li><a href="{COMPANY_WEBSITE}/careers">Careers & Partner Program</a></li>
        <li><a href="{COMPANY_WEBSITE}/ac-repair-{info['city_slug']}">AC Repair in {info['city']}</a></li>
        <li><a href="{COMPANY_WEBSITE}/electrician-{info['city_slug']}">Electrician in {info['city']}</a></li>
        <li><a href="{COMPANY_WEBSITE}/plumber-{info['city_slug']}">Plumber in {info['city']}</a></li>
    </ul>
    """
    full_content += internal_links

    # Backlinks
    backlink_html = "<h2>🔗 Trusted References</h2><ul>"
    for link in BACKLINK_SOURCES:
        backlink_html += f'<li><a href="{link["url"]}" target="_blank" rel="noopener">{link["text"]}</a></li>'
    backlink_html += "</ul>"
    full_content += backlink_html

    # Schema
    schema_jsonld = build_schema_jsonld(info, blog_data)
    full_content += f'<script type="application/ld+json">{schema_jsonld}</script>'
    if job_schema:
        full_content += f'<script type="application/ld+json">{json.dumps(job_schema, ensure_ascii=False)}</script>'

    # Category & tags
    category_id = get_category_id(info["category"])
    tag_ids = []
    for tag_name in (blog_data.get("tags") or [])[:5]:
        try:
            url = f"{WP_URL}/wp-json/wp/v2/tags"
            r = requests.get(url, params={"search": tag_name}, auth=(WP_USERNAME, WP_APP_PASSWORD))
            if r.status_code == 200 and r.json():
                tag_ids.append(r.json()[0]["id"])
            else:
                r = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json={"name": tag_name})
                if r.status_code == 201:
                    tag_ids.append(r.json()["id"])
        except:
            pass

    keyword = info.get("keyword", info["name"])
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
        r = requests.post(wp_api_url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=post_data, headers={"Content-Type": "application/json"})
        if r.status_code == 201:
            result = r.json()
            print(f"✅ Published: {blog_data['title']}")
            print(f"   URL: {result.get('link', '')}")
            print(f"   Category: {info['category']}")
            print(f"   Keyphrase: {keyword}")
            return result
        else:
            print(f"❌ WordPress Error: {r.status_code}")
            print(r.text)
            return None
    except Exception as e:
        print(f"❌ WordPress Error: {e}")
        return None


# =========================================================
# ============ MAIN =======================================
# =========================================================
def main():
    mode = os.getenv("BLOG_MODE", "both")  # 'service' | 'hiring' | 'both'
    today = datetime.datetime.now()

    # ---------- HIRING BLOG ----------
    if mode in ("hiring", "both"):
        role = HIRING_ROLES[today.day % len(HIRING_ROLES)]
        city = CITIES[today.day % len(CITIES)]

        print(f"💼 Hiring Blog: {role['name']} – {city['name']}")
        for lang in ("en", "hi"):
            data = generate_hiring_post(role["name"], city["name"], city["hi"], lang, role.get("gender", "any"))
            if data:
                info = {
                    "name": role["name"],
                    "category": role["category"],
                    "city": city["name"],
                    "city_hi": city["hi"],
                    "city_slug": city["slug"],
                    "keyword": f"{role['name']} job {city['name']}",
                    "slug": f"{role['name'].lower().replace(' ','-')}-job-{city['slug']}" + ("-hi" if lang == "hi" else ""),
                    "gender": role.get("gender", "any"),
                }
                publish_to_wordpress(data, info, job_schema=build_job_schema(role["name"], city["name"]), is_hiring=True)

    # ---------- SERVICE BLOG ----------
    if mode in ("service", "both"):
        seoni_day_index = today.day % len(SEONI_SERVICES)
        seoni_service = SEONI_SERVICES[seoni_day_index]

        other_services = [s for s in SERVICES if s["city"] != PRIORITY_CITY]
        other_index = today.day % len(other_services)
        other_service = other_services[other_index]

        for idx, svc in enumerate([seoni_service, other_service], 1):
            print(f"🤖 [EN] Service Blog {idx}: {svc['name']} - {svc['city']}")
            data_en = generate_blog_post(
                svc["name"], svc["keyword"], svc["city"], "en", svc["city_hi"],
                svc["visit_charge"], svc["localities_en"], svc["landmarks"], svc["warranty_eligible"]
            )
            if data_en:
                publish_to_wordpress(data_en, svc)

            print(f"🤖 [HI] Service Blog {idx}: {SERVICES_HI[svc['name']]} - {svc['city']}")
            data_hi = generate_blog_post(
                svc["name"], svc["keyword"], svc["city"], "hi", svc["city_hi"],
                svc["visit_charge"], svc["localities_hi"], svc["landmarks"], svc["warranty_eligible"]
            )
            if data_hi:
                service_hi = svc.copy()
                service_hi["category"] = svc["category"] + "-HI"
                service_hi["keyword"] = get_hindi_keyword(svc["name"], svc["city_hi"])
                publish_to_wordpress(data_hi, service_hi)


if __name__ == "__main__":
    main()
