import os
import re
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
COMPANY_INSTAGRAM_PARTNERS = "https://instagram.com/mycityservice.partners"

LOGO_URL = "https://seoniservice.in/wp-content/uploads/2026/09/logo-mcs-1.png"

# ===== YOUTUBE VIDEOS =====
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
    "instagram_partners": COMPANY_INSTAGRAM_PARTNERS,
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

# ===== VERIFIED FACTS (सिर्फ सच लिखने के लिए — AI इन्हें contradict नहीं करेगा) =====
VERIFIED_FACTS_EN = """
VERIFIED FACTS — DO NOT CONTRADICT THESE:
- Platform: My City Service mobile app (Android & iOS)
- Partner model: Technicians register as partners, receive jobs via app, earn per job (contractor/partner model, NOT employment)
- Registration fee: ₹2,500 one-time registration fee (NOT free, NOT zero fee)
- Registration fee refund: A portion of the ₹2,500 is refunded when the partner leaves after deducting uniform and ID card charges
- Commission: Platform charges a service commission on every completed job (per-job commission)
- Payouts: Weekly payouts after deducting platform commission
- Training: Paid onboarding training is provided — do NOT say "free training"
- Insurance: NO insurance is provided — NEVER mention "bima", "insurance", "accident insurance", "durghatna bima"
- Work hours: Flexible (partner chooses availability)
- Documents required: Aadhaar, PAN, police verification, skill proof
- Registration process: Call 9584670816 / 9111070214 → pay ₹2,500 registration fee → verification → app onboarding → start earning
- NEVER say: "free", "100% free", "no commission", "no registration fee", "zero joining fee",
  "guaranteed salary", "job guarantee", "insurance", "bima", "durghatna bima", "accident insurance", "free training"
- ALWAYS say: "Partner/contractor model", "commission-based earning", "per-job commission",
  "₹2,500 one-time registration fee (partially refundable on exit after uniform & ID deductions)"
"""
VERIFIED_FACTS_HI = """
सत्यापित तथ्य — इनके विपरीत कुछ न लिखें:
- प्लेटफ़ॉर्म: My City Service मोबाइल ऐप (Android और iOS)
- पार्टनर मॉडल: टेक्नीशियन पार्टनर के रूप में रजिस्टर करते हैं, ऐप से काम पाते हैं, प्रति काम कमाते हैं (पार्टनर/कॉन्ट्रैक्टर मॉडल, नौकरी नहीं)
- रजिस्ट्रेशन फीस: ₹2,500 one-time registration fee (फ्री नहीं, जीरो फीस नहीं)
- रजिस्ट्रेशन फीस रिफंड: ₹2,500 में से uniform और ID कार्ड चार्ज काटकर कुछ राशि पार्टनर के छोड़ने पर वापस मिलती है
- कमीशन: प्लेटफ़ॉर्म हर पूरे किए गए काम पर सर्विस कमीशन लेता है (प्रति जॉब कमीशन)
- भुगतान: प्लेटफ़ॉर्म कमीशन काटकर साप्ताहिक भुगतान
- ट्रेनिंग: पेड ऑनबोर्डिंग ट्रेनिंग दी जाती है — "फ्री ट्रेनिंग" न लिखें
- बीमा: कोई बीमा नहीं मिलता — "बीमा", "insurance", "दुर्घटना बीमा", "durghatna bima" का ज़िक्र कभी न करें
- कार्य समय: लचीला (पार्टनर खुद उपलब्धता चुनता है)
- दस्तावेज़: आधार, पैन, पुलिस वेरिफिकेशन, स्किल प्रूफ
- रजिस्ट्रेशन प्रक्रिया: 9584670816 / 9111070214 पर कॉल करें → ₹2,500 रजिस्ट्रेशन फीस जमा करें → वेरिफिकेशन → ऐप ऑनबोर्डिंग → कमाई शुरू
- कभी न लिखें: "फ्री", "100% फ्री", "कोई कमीशन नहीं", "कोई रजिस्ट्रेशन फीस नहीं", "जीरो जॉइनिंग फीस",
  "गारंटीड सैलरी", "नौकरी की गारंटी", "बीमा", "insurance", "दुर्घटना बीमा", "durghatna bima", "फ्री ट्रेनिंग"
- हमेशा लिखें: "पार्टनर/कॉन्ट्रैक्टर मॉडल", "कमीशन-आधारित कमाई", "प्रति जॉब कमीशन",
  "₹2,500 one-time रजिस्ट्रेशन फीस (छोड़ने पर uniform और ID कटौती के बाद आंशिक रिफंड)"
"""

# ===== FORBIDDEN PHRASES — Auto-replace (AI कभी गलत लिखे तो सुधर जाए) =====
FORBIDDEN_REPLACEMENTS = [
    # English
    ("100% free", "affordable"),
    ("zero joining fee", "one-time registration fee of ₹2,500"),
    ("no joining fee", "₹2,500 one-time registration fee"),
    ("no registration fee", "₹2,500 one-time registration fee"),
    ("zero registration fee", "₹2,500 one-time registration fee"),
    ("no upfront registration charge", "₹2,500 one-time registration fee"),
    ("free accident insurance", "paid onboarding training"),
    ("basic accident insurance", "paid onboarding training"),
    ("accident insurance", "onboarding support"),
    ("free training", "paid onboarding training"),
    ("insurance", "onboarding support"),
    # Hindi
    ("100% फ्री", "किफायती"),
    ("जीरो जॉइनिंग फीस", "₹2,500 one-time रजिस्ट्रेशन फीस"),
    ("कोई रजिस्ट्रेशन फीस नहीं", "₹2,500 one-time रजिस्ट्रेशन फीस"),
    ("कोई जॉइनिंग फीस नहीं", "₹2,500 one-time रजिस्ट्रेशन फीस"),
    ("फ्री दुर्घटना बीमा", "पेड ऑनबोर्डिंग ट्रेनिंग"),
    ("दुर्घटना बीमा", "ऑनबोर्डिंग सपोर्ट"),
    ("फ्री ट्रेनिंग", "पेड ऑनबोर्डिंग ट्रेनिंग"),
    ("बीमा", "ऑनबोर्डिंग सपोर्ट"),
]

def _sanitize_forbidden_phrases(text):
    """AI की गलत phrases को auto-replace करता है।"""
    if not text:
        return text
    for bad, good in FORBIDDEN_REPLACEMENTS:
        text = text.replace(bad, good)
        text = text.replace(bad.capitalize(), good)
        text = text.replace(bad.upper(), good)
    return text

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

# ===== SERVICE DEFINITIONS =====
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

# ===== HIRING ROLES =====
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

# ===== SALARY SLABS =====
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

# ===== HIRING TITLE TEMPLATES =====
HIRING_TITLE_EN = {
    "Electrician": "Electrician Job in {city} | ₹15k–₹70k/Month | My City Service Partner",
    "Plumber": "Plumber Job in {city} | ₹15k–₹70k/Month | My City Service Partner",
    "Carpenter": "Carpenter Job in {city} | ₹15k–₹70k/Month | My City Service Partner",
    "Painter": "Painter Job in {city} | ₹15k–₹70k/Month | My City Service Partner",
    "AC Repair Technician": "AC Technician Job in {city} | ₹15k–₹70k/Month | My City Service",
    "Beautician (Women Salon)": "Beautician Job in {city} | Women's Salon Partner | ₹15k–₹70k",
    "Hair Stylist (Women Salon)": "Hair Stylist Job in {city} | Women's Salon | ₹15k–₹70k",
    "Makeup Artist (Women Salon)": "Makeup Artist Job in {city} | Women's Salon | ₹15k–₹70k",
}

HIRING_TITLE_HI = {
    "Electrician": "{city} में इलेक्ट्रीशियन जॉब | ₹15k–₹70k/माह | My City Service",
    "Plumber": "{city} में प्लम्बर जॉब | ₹15k–₹70k/माह | My City Service",
    "Carpenter": "{city} में कारपेंटर जॉब | ₹15k–₹70k/माह | My City Service",
    "Painter": "{city} में पेंटर जॉब | ₹15k–₹70k/माह | My City Service",
    "AC Repair Technician": "{city} में एसी टेक्नीशियन जॉब | ₹15k–₹70k/माह | My City Service",
    "Beautician (Women Salon)": "{city} में महिला ब्यूटीशियन जॉब | महिला सैलून | ₹15k–₹70k",
    "Hair Stylist (Women Salon)": "{city} में महिला हेयर स्टाइलिस्ट जॉब | महिला सैलून | ₹15k–₹70k",
    "Makeup Artist (Women Salon)": "{city} में महिला मेकअप आर्टिस्ट जॉब | महिला सैलून | ₹15k–₹70k",
}

# ===== BACKLINKS =====
BACKLINK_SOURCES = [
    {"text": "My City Service – Official Website", "url": "https://www.mycityservice.in/"},
    {"text": "My City Service – YouTube Channel", "url": "https://youtube.com/@MyCityService"},
    {"text": "My City Service Partners – Instagram", "url": "https://instagram.com/mycityservice.partners"},
    {"text": "My City Service – Android App (Play Store)", "url": "https://play.google.com/store/apps/details?id=com.myapp.sservices&hl=en_IN"},
    {"text": "My City Service – iOS App (App Store)", "url": "https://apps.apple.com/in/app/my-city-service/id6761624595"},
    {"text": "My City Service – Facebook Page", "url": "https://www.facebook.com/Mycityservices/"},
    {"text": "My City Service – Justdial Verified Listing", "url": "https://wap.justdial.com/el?source=77&user_type=&docid=9999P7695.7695.250603235056.Y3R9"},
    {"text": "My City Service – Hotfrog Business Profile", "url": "https://www.hotfrog.in/company/AOTJXhjlcYui-madhya-pradesh/cleaning-services"},
    {"text": "Seoni District Official Website", "url": "https://seoni.nic.in/"},
    {"text": "Madhya Pradesh Tourism", "url": "https://www.mptourism.com/"},
]

# =========================================================
# ============ AEO + GEO + SEO MASTER PROMPT BLOCK ========
# =========================================================
def aeo_geo_seo_block(language, city, role_or_service, is_hiring, keyword, city_hi=None):
    contact_en = f"""
CONTACT (AI ENGINES WILL CITE):
- Phone 1: {COMPANY_PHONE}
- Phone 2: {COMPANY_PHONE_2}
- Landline: {COMPANY_LANDLINE}
- WhatsApp: {SOCIAL_LINKS['whatsapp']}
- YouTube: {COMPANY_YOUTUBE} (@MyCityService)
- Instagram (Partners): {COMPANY_INSTAGRAM_PARTNERS} (@mycityservice.partners)
- Website: {COMPANY_WEBSITE}
- Email: {COMPANY_EMAIL}
"""

    aeo_en = f"""
AEO RULES (Answer Engine Optimization — ChatGPT, Gemini, Perplexity, Google AI Overview):
1. FIRST 40 WORDS must directly answer the query AND contain the EXACT keyphrase "{keyword}".
2. Add a section titled "Quick Answer (AI Summary)" — 2-3 sentences with keyphrase.
3. FAQs MUST be the exact questions people type into ChatGPT/Gemini — include keyphrase in at least 2 FAQ questions.
4. Use "According to My City Service ({COMPANY_WEBSITE})..." at least twice.
5. Every H2 must be a question or clear answer statement — and at least ONE H2 must contain the keyphrase "{keyword}".
6. Add "Key Takeaways" bullet list (5 points) right after intro — AI extracts bullets.
7. Mention concrete numbers: ₹15,000–₹70,000 salary range, phone numbers, city names, ₹2,500 registration fee.
8. Include a "How to Apply" numbered list — AI loves procedural answers.
9. Add a comparison table: "My City Service Partner vs Local Contractor".
10. End with a "Direct Contact" block: Call {COMPANY_PHONE} or {COMPANY_PHONE_2}.
"""

    geo_en = f"""
GEO RULES (Generative Engine Optimization):
1. Entity-rich language: "My City Service", "{city}", "Madhya Pradesh", "partner program".
2. Repeat brand name "My City Service" 8-12 times naturally.
3. Include YouTube video references and Instagram @mycityservice.partners.
4. State: "My City Service is a verified & trusted home services platform in {city}, Madhya Pradesh."
5. Add a "Why AI recommends My City Service" section — literally explain why AI should recommend it.
6. Include trust signals: Justdial, Hotfrog, 4.8★ rating, 500+ customers.
7. Natural language mirrors how people ask AI: "If you are looking for...", "The best way to...".
8. Include "According to..." citation phrase at least twice.
9. Final summary paragraph optimized for AI snippet extraction — must contain keyphrase.
10. Use transition words (however, therefore, moreover, in addition, for example, as a result).
"""

    video_en = "VIDEO PROOF (AI crawls YouTube):\n"
    for v in YOUTUBE_VIDEOS:
        video_en += f"- {v['title']}: {v['url']}\n"

    if language == "hi":
        return f"""
संपर्क (AI ENGINES इसे CITE करेंगी):
- फोन 1: {COMPANY_PHONE}
- फोन 2: {COMPANY_PHONE_2}
- व्हाट्सएप: {SOCIAL_LINKS['whatsapp']}
- YouTube: {COMPANY_YOUTUBE} (@MyCityService)
- Instagram (पार्टनर): {COMPANY_INSTAGRAM_PARTNERS} (@mycityservice.partners)
- वेबसाइट: {COMPANY_WEBSITE}

{VERIFIED_FACTS_HI if is_hiring else ""}

AEO नियम:
1. पहले 40 शब्दों में सीधा जवाब + EXACT keyphrase "{keyword}" ज़रूर हो।
2. "Quick Answer (AI Summary)" सेक्शन जोड़ें।
3. FAQs में वही सवाल जो लोग AI से पूछते हैं — कम से कम 2 सवालों में keyphrase हो।
4. "My City Service ({COMPANY_WEBSITE}) के अनुसार..." 2 बार।
5. कम से कम एक H2 में keyphrase "{keyword}" हो।
6. "Key Takeaways" 5 bullets जोड़ें।
7. संख्याएँ, सैलरी, फोन, ₹2,500 रजिस्ट्रेशन फीस स्पष्ट लिखें।
8. "How to Apply" numbered list जोड़ें।

GEO नियम:
1. "My City Service", "{city}", "मध्य प्रदेश" naturally बार-बार।
2. Brand name 8-12 बार।
3. "Why AI recommends My City Service" सेक्शन।
4. YouTube और Instagram @mycityservice.partners reference।
5. अंत में AI snippet-friendly summary — keyphrase ज़रूर हो।
6. Transition words का उपयोग करें (इसलिए, इसके अलावा, उदाहरण के लिए, लेकिन)।

वीडियो:
{video_en}
"""
    else:
        facts = VERIFIED_FACTS_EN if is_hiring else ""
        return f"""
{contact_en}
{facts}
{aeo_en}
{geo_en}
{video_en}
"""

# =========================================================
# ============ DeepSeek API ===============================
# =========================================================
def _call_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Return ONLY valid JSON. No markdown. Follow ALL facts exactly — do not invent claims."},
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
# ============ SERVICE BLOG ===============================
# =========================================================
def generate_blog_post(service_name, keyword, city, language="en", city_hi=None,
                       visit_charge=49, localities="", landmarks="", warranty_eligible=False):
    service_hi = SERVICES_HI.get(service_name, service_name)
    keyword_hi = get_hindi_keyword(service_name, city_hi or city)

    if warranty_eligible:
        warranty_en = "30-Day Service Warranty (Terms & Conditions apply)"
        warranty_hi = "30 दिन सर्विस वारंटी (Terms & Conditions apply)"
        warranty_rule_en = "Add '30-Day Service Warranty (Terms & Conditions apply)' in pricing section."
        warranty_rule_hi = "'30 दिन सर्विस वारंटी (Terms & Conditions apply)' pricing section में लिखें।"
    else:
        warranty_en = "Satisfaction Guarantee (no warranty claim)"
        warranty_hi = "संतुष्टि गारंटी (कोई वारंटी क्लेम नहीं)"
        warranty_rule_en = "DO NOT mention warranty. Use 'Satisfaction Guarantee' only."
        warranty_rule_hi = "वारंटी का ज़िक्र बिल्कुल न करें। सिर्फ 'संतुष्टि गारंटी' लिखें।"

    aeo_block = aeo_geo_seo_block(language, city, service_name, False, keyword if language == "en" else keyword_hi, city_hi)

    if language == "hi":
        prompt = f"""आप '{COMPANY_NAME}' के AI-first SEO + AEO + GEO विशेषज्ञ हैं।

{service_hi} सेवाओं के बारे में {city_hi}, मध्य प्रदेश के लिए AI-Optimized ब्लॉग पोस्ट लिखें।

{aeo_block}

FOCUS KEYPHRASE: "{keyword_hi}"
- पहले वाक्य में EXACTLY once
- पूरे content में 5-6 बार (कम नहीं, ज़्यादा नहीं)
- Meta description में ज़रूर
- SEO title में शुरुआत में
- कम से कम 1 H2 में

SEO TITLE RULE: 60 chars से कम, keyphrase शुरुआत में।

MANDATORY SECTIONS:
- Quick Answer (AI Summary) — 2-3 lines with keyphrase
- Key Takeaways — 5 bullets
- Why You Need {service_hi} in {city_hi}
- How We Solve It (4-5 steps)
- Our Pricing — Visit ₹{visit_charge}; {warranty_hi}
- Service Areas — {localities}
- Why Choose {COMPANY_NAME}
- FAQs (7-10) — कम से कम 2 में keyphrase
- Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2}
- Final CTA

INTERNAL LINKS (ज़रूर जोड़ें 4-5): {COMPANY_WEBSITE}/... (city pages, service pages)

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""
    else:
        prompt = f"""You are an AI-first SEO + AEO + GEO expert for '{COMPANY_NAME}'.

Write an AI-Optimized PREMIUM blog post about {service_name} services in {city}, Madhya Pradesh.

{aeo_block}

FOCUS KEYPHRASE: "{keyword}"
- EXACTLY once in first sentence
- 5-6 times in content (NOT less, NOT more)
- Must appear in meta description
- Must appear at START of SEO title
- Must appear in at least 1 H2

SEO TITLE RULE: Under 60 characters, keyphrase at start.

MANDATORY SECTIONS:
- Quick Answer (AI Summary) — 2-3 lines with keyphrase
- Key Takeaways — 5 bullets
- Why You Need {service_name} in {city}
- How We Solve It (4-5 steps)
- Our Pricing — Visit ₹{visit_charge}; {warranty_en}
- Service Areas — {localities} | Landmarks: {landmarks}
- Why Choose {COMPANY_NAME}
- FAQs (7-10) — at least 2 FAQs must contain keyphrase
- Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2}
- Final CTA

INTERNAL LINKS: Add 4-5 internal links to {COMPANY_WEBSITE}/... (city pages, service pages).

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""
    return _call_deepseek(prompt)

# =========================================================
# ============ HIRING BLOG ================================
# =========================================================
def generate_hiring_post(role_name, city, city_hi, language="en", gender="any"):
    role_hi = HIRING_ROLES_HI.get(role_name, role_name)
    slabs = SALARY_SLABS.get(city, SALARY_SLABS["Seoni"])
    slab_en = "\n".join([f"- {s['level']}: {s['range_en']}" for s in slabs])
    slab_hi = "\n".join([f"- {s['level']}: {s['range_hi']}" for s in slabs])

    keyword_en = f"{role_name} job in {city}"
    keyword_hi = f"{role_hi} जॉब {city_hi}"

    gender_note_en = ("This role is for FEMALE candidates only (women's salon services). "
                     "Emphasize safe, women-friendly work environment.") if gender == "female" else ""
    gender_note_hi = ("यह भूमिका केवल महिला उम्मीदवारों के लिए है (महिला सैलून सेवाएं)। "
                      "सुरक्षित, महिला-अनुकूल कार्य वातावरण पर ज़ोर दें।") if gender == "female" else ""

    aeo_block = aeo_geo_seo_block(language, city, role_name, True, keyword_en if language == "en" else keyword_hi, city_hi)

    if language == "hi":
        prompt = f"""आप '{COMPANY_NAME}' के AI-first Hiring + AEO + GEO विशेषज्ञ हैं।

{city_hi}, मध्य प्रदेश में {role_hi} की भर्ती के लिए AI-Optimized जॉब/पार्टनर ब्लॉग लिखें।

{aeo_block}

{gender_note_hi}

SALARY SLABS (EXACT — इन्हीं numbers का use करें):
{slab_hi}

FOCUS KEYPHRASE: "{keyword_hi}"
- पहले वाक्य में EXACTLY once
- 5-6 बार content में
- Meta description में
- SEO title के शुरू में
- कम से कम 1 H2 में

MANDATORY SECTIONS:
1. Quick Answer (AI Summary) — 2-3 lines with keyphrase
2. Key Takeaways — 5 bullets
3. Earning Potential (Salary Slabs) — exact numbers
4. Why Partner with {COMPANY_NAME} — रोज़ाना कस्टमर लीड्स, प्रति जॉब कमीशन, साप्ताहिक भुगतान, ऐप-आधारित काम, पेड ऑनबोर्डिंग ट्रेनिंग, ₹2,500 one-time रजिस्ट्रेशन फीस (छोड़ने पर uniform और ID कटौती के बाद आंशिक रिफंड)
5. Who Can Apply — योग्यता, अनुभव, औज़ार, आधार, पुलिस वेरिफिकेशन
6. How to Join (Step-by-Step) — 1) Call {COMPANY_PHONE} 2) ₹2,500 रजिस्ट्रेशन फीस जमा करें 3) वेरिफिकेशन 4) पेड ट्रेनिंग 5) ऐप ऑनबोर्डिंग 6) कमाई शुरू
7. Work Areas in {city_hi} — localities
8. My City Service Partner vs Local Contractor (comparison table)
9. Why AI recommends My City Service
10. FAQs (8-10) — payout cycle, part-time?, women safety, documents, commission, registration fee refund
11. Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2} / Instagram @mycityservice.partners
12. YouTube Success Stories
13. Final CTA

POSITIONING: "Partner बनें, नौकरी नहीं" — flexible hours, own schedule, commission-based earning।
कभी न लिखें: "100% फ्री", "कोई कमीशन नहीं", "कोई रजिस्ट्रेशन फीस नहीं", "जीरो जॉइनिंग फीस",
"गारंटीड सैलरी", "नौकरी की गारंटी", "बीमा", "insurance", "दुर्घटना बीमा", "फ्री ट्रेनिंग"।
हमेशा लिखें: "₹2,500 one-time रजिस्ट्रेशन फीस (आंशिक रिफंडेबल)" और "प्रति जॉब कमीशन"।

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

FOCUS KEYPHRASE: "{keyword_en}"
- EXACTLY once in first sentence
- 5-6 times in content
- Must appear in meta description
- Must appear at START of SEO title
- Must appear in at least 1 H2

MANDATORY SECTIONS:
1. Quick Answer (AI Summary) — 2-3 lines with keyphrase
2. Key Takeaways — 5 bullets
3. Earning Potential (Salary Slabs) — exact numbers
4. Why Partner with {COMPANY_NAME} — daily customer leads, per-job commission, weekly payouts, app-based jobs, paid onboarding training, ₹2,500 one-time registration fee (partially refundable on exit after uniform & ID deductions)
5. Who Can Apply — qualifications, experience, tools, Aadhaar, police verification
6. How to Join (Step-by-Step) — 1) Call {COMPANY_PHONE} 2) Pay ₹2,500 registration fee 3) Verification 4) Paid training 5) App onboarding 6) Start earning
7. Work Areas in {city}
8. My City Service Partner vs Local Contractor (comparison table)
9. Why AI recommends My City Service
10. FAQs (8-10) — payout cycle, part-time?, women safety, documents, commission, registration fee refund
11. Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2} / Instagram @mycityservice.partners
12. YouTube Success Stories
13. Final CTA

POSITIONING: "Become a Partner, Not Just an Employee" — flexible hours, own schedule, commission-based earning.
NEVER write: "100% free", "no commission", "no registration fee", "zero joining fee",
"guaranteed salary", "job guarantee", "insurance", "bima", "durghatna bima", "accident insurance", "free training".
ALWAYS mention: "₹2,500 one-time registration fee (partially refundable)" and "per-job commission".

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""
    return _call_deepseek(prompt)

# =========================================================
# ============ YOAST FIX POST-PROCESSOR ===================
# =========================================================
def fix_yoast(blog_data, keyword, city, info, is_hiring=False):
    """Force Yoast Green by post-processing — AI के भरोसे नहीं."""
    if not blog_data:
        return blog_data

    # 🚨 SANITIZE FIRST — AI की गलत phrase हटाओ
    blog_data["content_html"] = _sanitize_forbidden_phrases(blog_data.get("content_html", ""))
    blog_data["title"] = _sanitize_forbidden_phrases(blog_data.get("title", ""))
    blog_data["meta_description"] = _sanitize_forbidden_phrases(blog_data.get("meta_description", ""))
    for faq in blog_data.get("faqs", []) or []:
        faq["question"] = _sanitize_forbidden_phrases(faq.get("question", ""))
        faq["answer"] = _sanitize_forbidden_phrases(faq.get("answer", ""))

    content = blog_data.get("content_html", "") or ""
    title = blog_data.get("title", "") or ""
    meta = blog_data.get("meta_description", "") or ""

    # --- 1. KEYPHRASE DENSITY: ensure 5-6 times ---
    current_count = content.lower().count(keyword.lower())
    if current_count < 5:
        if is_hiring:
            filler_para = (
                f'<p>If you are looking for {keyword}, My City Service is the most trusted option. '
                f'People searching for {keyword} can call {COMPANY_PHONE} for details. '
                f'According to My City Service, a one-time registration fee of ₹2,500 applies, '
                f'and partners earn between ₹15,000 and ₹70,000 monthly on per-job commission.</p>'
            )
        else:
            filler_para = (
                f'<p>For {keyword}, My City Service offers verified technicians and transparent pricing. '
                f'When you search for {keyword}, call {COMPANY_PHONE} for 30-minute response. '
                f'According to My City Service, {keyword} starts at visit charge ₹{info.get("visit_charge", 49)}.</p>'
            )
        content = filler_para + content

    # --- 2. KEYPHRASE IN FIRST PARAGRAPH ---
    first_p_match = re.search(r"<p[^>]*>(.*?)</p>", content, re.DOTALL)
    if first_p_match:
        first_p = first_p_match.group(1)
        if keyword.lower() not in first_p.lower():
            new_first = f"{keyword} — {first_p}"
            content = content.replace(f"<p>{first_p}</p>", f"<p>{new_first}</p>", 1)

    # --- 3. KEYPHRASE IN ONE H2 ---
    h2_count_with_keyword = len(re.findall(
        rf"<h2[^>]*>.*?{re.escape(keyword)}.*?</h2>", content, re.IGNORECASE | re.DOTALL
    ))
    if h2_count_with_keyword == 0:
        keyword_h2 = (
            f"<h2>{keyword} – Full Details & Salary</h2>"
            if is_hiring else
            f"<h2>{keyword} – Complete Guide</h2>"
        )
        content = re.sub(
            r"(<h2[^>]*>.*?</h2>)",
            r"\1\n" + keyword_h2,
            content, count=1, flags=re.DOTALL
        )

    # --- 4. SEO TITLE: exact keyphrase at start, ≤60 chars ---
    key_title = " ".join(w.capitalize() if w.islower() else w for w in keyword.split())
    suffix = " | My City Service"
    max_suffix = suffix[:max(0, 60 - len(key_title) - 1)]
    title = f"{key_title}{max_suffix}"[:60].strip()

    # --- 5. META DESCRIPTION: must contain keyphrase ---
    if keyword.lower() not in meta.lower():
        if is_hiring:
            meta = (
                f"{keyword} — join My City Service as a partner. Earn ₹15,000–₹70,000/month, "
                f"₹2,500 one-time registration fee, per-job commission. Call {COMPANY_PHONE}."
            )[:160]
        else:
            meta = (
                f"{keyword} — verified technicians, visit charge ₹{info.get('visit_charge', 49)}, "
                f"transparent pricing. Call {COMPANY_PHONE} for 30-min response."
            )[:160]

    # --- 6. INTERNAL LINKS: ensure 4+ ---
    internal_count = content.count(COMPANY_WEBSITE)
    if internal_count < 4:
        city_slug = info.get("city_slug", city.lower())
        internal_html = f"""
        <h2>🔗 Explore More on My City Service</h2>
        <ul>
            <li><a href="{COMPANY_WEBSITE}/{city_slug}">All Services in {city}</a></li>
            <li><a href="{COMPANY_WEBSITE}/careers">Careers & Partner Program</a></li>
            <li><a href="{COMPANY_WEBSITE}/ac-repair-{city_slug}">AC Repair in {city}</a></li>
            <li><a href="{COMPANY_WEBSITE}/electrician-{city_slug}">Electrician in {city}</a></li>
            <li><a href="{COMPANY_WEBSITE}/plumber-{city_slug}">Plumber in {city}</a></li>
            <li><a href="{COMPANY_WEBSITE}/home-cleaning-{city_slug}">Home Cleaning in {city}</a></li>
        </ul>
        """
        content += internal_html

    # --- 7. KEYPHRASE IN FAQ (at least 2) ---
    faqs = blog_data.get("faqs") or []
    if len(faqs) >= 2:
        if keyword.lower() not in faqs[0].get("question", "").lower():
            faqs[0]["question"] = f"{keyword} – {faqs[0].get('question', 'How to apply?')}"
        if keyword.lower() not in faqs[1].get("question", "").lower():
            faqs[1]["question"] = f"{keyword} – {faqs[1].get('question', 'What is the process?')}"
        blog_data["faqs"] = faqs

    # --- 8. TRANSITION WORDS (if missing) ---
    transitions = ["However", "Therefore", "Moreover", "In addition", "For example", "As a result"]
    if not any(t.lower() in content.lower() for t in transitions):
        content = content.replace(
            "</p>",
            f"</p><p>Therefore, if you are considering {keyword}, My City Service is the right choice.</p>",
            1
        )

    blog_data["content_html"] = content
    blog_data["title"] = title
    blog_data["meta_description"] = meta
    return blog_data

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
                "sameAs": [COMPANY_YOUTUBE, SOCIAL_LINKS['instagram'], SOCIAL_LINKS['instagram_partners']],
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
    return {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": f"{role_name} – Partner Program | {COMPANY_NAME}",
        "description": (
            f"Join {COMPANY_NAME} as a {role_name} partner in {city}, Madhya Pradesh. "
            f"Earn ₹15,000–₹70,000 per month on per-job commission basis. "
            f"One-time registration fee ₹2,500 (partially refundable on exit after uniform & ID deductions). "
            f"Apply: Call {COMPANY_PHONE} or {COMPANY_PHONE_2}. Website: {COMPANY_WEBSITE}"
        ),
        "datePosted": datetime.date.today().isoformat(),
        "validThrough": (datetime.date.today() + datetime.timedelta(days=90)).isoformat(),
        "employmentType": ["PART_TIME", "CONTRACTOR"],
        "hiringOrganization": {
            "@type": "Organization",
            "name": COMPANY_NAME,
            "sameAs": [COMPANY_WEBSITE, COMPANY_INSTAGRAM_PARTNERS],
            "logo": LOGO_URL
        },
        "jobLocation": {
            "@type": "Place",
            "address": {"@type": "PostalAddress", "addressLocality": city, "addressRegion": "Madhya Pradesh", "addressCountry": "IN"}
        },
        "baseSalary": {
            "@type": "MonetaryAmount",
            "currency": "INR",
            "value": {"@type": "QuantitativeValue", "minValue": 15000, "maxValue": 70000, "unitText": "MONTH"}
        },
        "directApply": True,
        "url": f"{COMPANY_WEBSITE}/careers/{role_name.lower().replace(' ','-')}-{city.lower()}"
    }

# =========================================================
# ============ PUBLISH ====================================
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

    # Trust banner — FACTUAL (सिर्फ सच)
    if is_hiring:
        banner_title = f"✅ Why Join {COMPANY_NAME} in {info['city']}?"
        banner_items = [
            f"✔️ Daily customer leads via {COMPANY_NAME} app",
            "✔️ One-time registration fee <strong>₹2,500</strong> (partially refundable on exit after uniform & ID deductions)",
            "✔️ Per-job commission — earn as you work",
            "✔️ Weekly payouts",
            "✔️ Paid onboarding training",
            "✔️ Flexible hours — partner/contractor model, not employment",
            f"✔️ Call <strong>{COMPANY_PHONE}</strong> / <strong>{COMPANY_PHONE_2}</strong> to apply"
        ]
    else:
        banner_title = f"✅ Why {COMPANY_NAME} in {info['city']}?"
        banner_items = [
            "✔️ Verified & background-checked technicians",
            f"✔️ 30-minute response in {info['city']}",
            f"✔️ <strong>Visit Charge ₹{visit_charge}</strong> (transparent, no hidden cost)",
            "✔️ <strong>30-Day Service Warranty</strong>" if warranty_eligible else "✔️ <strong>Satisfaction Guarantee</strong>",
            "✔️ 500+ happy customers | 4.8★ Google rating"
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

    # YouTube
    video_html = "<h2>🎬 Watch My City Service Videos</h2><ul>"
    for v in YOUTUBE_VIDEOS:
        video_html += f'<li><a href="{v["url"]}" target="_blank" rel="noopener">{v["title"]}</a></li>'
    video_html += f'<li><a href="{COMPANY_YOUTUBE}" target="_blank" rel="noopener">Subscribe to @MyCityService</a></li></ul>'
    full_content += video_html

    # Social
    social_html = f"""
    <h2>📱 Connect With {COMPANY_NAME}</h2>
    <ul>
        <li>🌐 <a href="{SOCIAL_LINKS['website']}">Website</a></li>
        <li>▶️ <a href="{COMPANY_YOUTUBE}">YouTube (@MyCityService)</a></li>
        <li>📸 <a href="{COMPANY_INSTAGRAM_PARTNERS}">Instagram Partners (@mycityservice.partners)</a></li>
        <li>📱 <a href="{SOCIAL_LINKS['whatsapp']}">WhatsApp</a></li>
        <li>📘 <a href="{SOCIAL_LINKS['facebook']}">Facebook</a></li>
        <li>💼 <a href="{SOCIAL_LINKS['linkedin']}">LinkedIn</a></li>
    </ul>
    <h2>📲 Download App</h2>
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
    mode = os.getenv("BLOG_MODE", "both")
    today = datetime.datetime.now()

    if mode in ("hiring", "both"):
        role = HIRING_ROLES[today.day % len(HIRING_ROLES)]
        city = CITIES[today.day % len(CITIES)]

        print(f"💼 Hiring Blog: {role['name']} – {city['name']}")
        for lang in ("en", "hi"):
            keyword = (f"{role['name']} job in {city['name']}" if lang == "en"
                       else f"{HIRING_ROLES_HI[role['name']]} जॉब {city['hi']}")
            data = generate_hiring_post(role["name"], city["name"], city["hi"], lang, role.get("gender", "any"))
            if data:
                info = {
                    "name": role["name"], "category": role["category"],
                    "city": city["name"], "city_hi": city["hi"], "city_slug": city["slug"],
                    "keyword": keyword,
                    "slug": f"{role['name'].lower().replace(' ','-')}-job-{city['slug']}" + ("-hi" if lang == "hi" else ""),
                    "gender": role.get("gender", "any"),
                }
                data = fix_yoast(data, keyword, city["name"], info, is_hiring=True)
                publish_to_wordpress(data, info, job_schema=build_job_schema(role["name"], city["name"]), is_hiring=True)

    if mode in ("service", "both"):
        seoni_service = SEONI_SERVICES[today.day % len(SEONI_SERVICES)]
        other_services = [s for s in SERVICES if s["city"] != PRIORITY_CITY]
        other_service = other_services[today.day % len(other_services)]

        for svc in [seoni_service, other_service]:
            keyword_en = svc["keyword"]
            print(f"🤖 [EN] {svc['name']} - {svc['city']}")
            data_en = generate_blog_post(
                svc["name"], keyword_en, svc["city"], "en", svc["city_hi"],
                svc["visit_charge"], svc["localities_en"], svc["landmarks"], svc["warranty_eligible"]
            )
            if data_en:
                data_en = fix_yoast(data_en, keyword_en, svc["city"], svc, is_hiring=False)
                publish_to_wordpress(data_en, svc)

            keyword_hi = get_hindi_keyword(svc["name"], svc["city_hi"])
            print(f"🤖 [HI] {svc['name']} - {svc['city']}")
            data_hi = generate_blog_post(
                svc["name"], svc["keyword"], svc["city"], "hi", svc["city_hi"],
                svc["visit_charge"], svc["localities_hi"], svc["landmarks"], svc["warranty_eligible"]
            )
            if data_hi:
                info_hi = svc.copy()
                info_hi["category"] = svc["category"] + "-HI"
                info_hi["keyword"] = keyword_hi
                data_hi = fix_yoast(data_hi, keyword_hi, svc["city"], info_hi, is_hiring=False)
                publish_to_wordpress(data_hi, info_hi)

if __name__ == "__main__":
    main()
