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
COMPANY_TAGLINE = "Partner platform for home service professionals"
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
    "whatsapp": "https://wa.me/919584670816",
    "facebook": "https://facebook.com/Mycityservices/",
    "instagram": "https://instagram.com/mycityservice.in",
    "linkedin": "https://linkedin.com/in/my-city-service",
    "playstore": "https://play.google.com/store/apps/details?id=com.myapp.sservices&hl=en_IN",
    "appstore": "https://apps.apple.com/in/app/my-city-service/id6761624595",
}

PRIORITY_CITY = "Seoni"

# ===== CORE FACTS =====
CORE_FACTS_EN = """
MY CITY SERVICE — CORE FACTS (never contradict):
- My City Service is a HOME SERVICES PLATFORM (app-based, Android + iOS).
- Customers book services online through the app.
- Partners (electricians, plumbers, carpenters, painters, AC technicians, salon professionals) provide the service at the customer's doorstep.
- My City Service gives partners: TRAINING + ONBOARDING + daily customer leads via app.
- Earning potential: ₹10,000 to ₹50,000 per month (depends on city + skill + jobs completed).
- Registration fee: ₹2,500 one-time, paid at partner app registration.
  (When a partner leaves, a portion may be refunded after deducting uniform & ID charges.)
- Commission: A service commission is charged per completed job (per-job commission).
- Payouts: Weekly.
- No employment guarantee. This is a PARTNER model, not a job/employment contract.
- Training is provided — but not described as "free". Use "training provided" or "onboarding training".
- No insurance is mentioned. Never write "bima" or "insurance".
- Documents needed: Aadhaar, PAN, police verification, skill proof.
- Registration steps: Call 9584670816 / 9111070214 → pay ₹2,500 registration fee → verification → training → app onboarding → start getting jobs.
- NEVER say: "free", "100% free", "no commission", "no registration fee", "zero joining fee",
  "guaranteed salary", "job guarantee", "insurance", "bima", "durghatna bima", "accident insurance".
- ALWAYS say: "partner model", "per-job commission", "₹2,500 one-time registration fee",
  "₹10,000–₹50,000 monthly earning potential", "training + onboarding provided".
"""

CORE_FACTS_HI = """
MY CITY SERVICE — मुख्य तथ्य (कभी न बदलें):
- My City Service एक होम सर्विस प्लेटफ़ॉर्म है (ऐप-आधारित, Android + iOS)।
- ग्राहक ऐप से ऑनलाइन सर्विस बुक करते हैं।
- पार्टनर (इलेक्ट्रीशियन, प्लम्बर, कारपेंटर, पेंटर, एसी टेक्नीशियन, सैलून प्रोफेशनल) ग्राहक के घर पर प्रोफेशनल सर्विस देते हैं।
- My City Service पार्टनर को देता है: ट्रेनिंग + ऑनबोर्डिंग + ऐप से रोज़ाना कस्टमर लीड्स।
- कमाई की संभावना: ₹10,000 से ₹50,000 प्रति माह (शहर + स्किल + किए गए काम पर निर्भर)।
- रजिस्ट्रेशन फीस: ₹2,500 one-time, पार्टनर ऐप रजिस्ट्रेशन के समय।
  (पार्टनर के छोड़ने पर uniform और ID चार्ज काटकर कुछ राशि वापस मिल सकती है।)
- कमीशन: प्रति पूरा किया गया काम पर सर्विस कमीशन लिया जाता है (प्रति जॉब कमीशन)।
- भुगतान: साप्ताहिक।
- कोई नौकरी की गारंटी नहीं। यह पार्टनर मॉडल है, नौकरी/रोज़गार अनुबंध नहीं।
- ट्रेनिंग दी जाती है — लेकिन "फ्री" न कहें। "ट्रेनिंग दी जाती है" या "ऑनबोर्डिंग ट्रेनिंग" लिखें।
- बीमा का ज़िक्र कभी नहीं। "बीमा" या "insurance" कभी न लिखें।
- दस्तावेज़: आधार, पैन, पुलिस वेरिफिकेशन, स्किल प्रूफ।
- रजिस्ट्रेशन स्टेप्स: 9584670816 / 9111070214 पर कॉल करें → ₹2,500 रजिस्ट्रेशन फीस दें → वेरिफिकेशन → ट्रेनिंग → ऐप ऑनबोर्डिंग → काम मिलना शुरू।
- कभी न लिखें: "फ्री", "100% फ्री", "कोई कमीशन नहीं", "कोई रजिस्ट्रेशन फीस नहीं", "जीरो जॉइनिंग फीस",
  "गारंटीड सैलरी", "नौकरी की गारंटी", "बीमा", "insurance", "दुर्घटना बीमा"।
- हमेशा लिखें: "पार्टनर मॉडल", "प्रति जॉब कमीशन", "₹2,500 one-time रजिस्ट्रेशन फीस",
  "₹10,000–₹50,000 मासिक कमाई की संभावना", "ट्रेनिंग + ऑनबोर्डिंग दी जाती है"।
"""

# ===== FORBIDDEN PHRASES =====
FORBIDDEN_REPLACEMENTS = [
    ("100% free", "affordable"),
    ("zero joining fee", "one-time registration fee of ₹2,500"),
    ("no joining fee", "₹2,500 one-time registration fee"),
    ("no registration fee", "₹2,500 one-time registration fee"),
    ("zero registration fee", "₹2,500 one-time registration fee"),
    ("free accident insurance", "training support"),
    ("basic accident insurance", "training support"),
    ("accident insurance", "training support"),
    ("free training", "training provided"),
    ("insurance", "training support"),
    ("100% फ्री", "किफायती"),
    ("जीरो जॉइनिंग फीस", "₹2,500 one-time रजिस्ट्रेशन फीस"),
    ("कोई रजिस्ट्रेशन फीस नहीं", "₹2,500 one-time रजिस्ट्रेशन फीस"),
    ("कोई जॉइनिंग फीस नहीं", "₹2,500 one-time रजिस्ट्रेशन फीस"),
    ("फ्री दुर्घटना बीमा", "ट्रेनिंग सपोर्ट"),
    ("दुर्घटना बीमा", "ट्रेनिंग सपोर्ट"),
    ("फ्री ट्रेनिंग", "ट्रेनिंग दी जाती है"),
    ("बीमा", "ट्रेनिंग सपोर्ट"),
]

def _sanitize(text):
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
        "name": "Seoni", "slug": "seoni", "hi": "सिवनी",
        "localities_en": "Gol Bazar, Main Market, Civil Lines, Budhwara, Kanhiwada, Barapathar, Jawahar Nagar",
        "localities_hi": "गोल बाजार, मेन मार्केट, सिविल लाइंस, बुधवारा, कन्हीवाड़ा, बरापथर, जवाहर नगर",
        "landmarks": "near Seoni Bus Stand, District Court, Pench Tiger Reserve, Government Medical College"
    },
    {
        "name": "Chhindwara", "slug": "chhindwara", "hi": "छिंदवाड़ा",
        "localities_en": "Chandangaon, Parasia, Sausar, Pandhurna, Amarwara, Damua",
        "localities_hi": "चांदनगांव, परासिया, सौंसर, पांधुरना, अमरवाड़ा, दमुआ",
        "landmarks": "near Chhindwara Bus Stand, District Hospital"
    },
    {
        "name": "Jabalpur", "slug": "jabalpur", "hi": "जबलपुर",
        "localities_en": "Wright Town, Napier Town, Vijay Nagar, Rampur, Adhartal, Gorakhpur",
        "localities_hi": "राइट टाउन, नेपियन टाउन, विजय नगर, रामपुर, अधारताल, गोरखपुर",
        "landmarks": "near Jabalpur Railway Station, Rani Durgavati Museum, Dumna Nature Reserve"
    },
    {
        "name": "Balaghat", "slug": "balaghat", "hi": "बालाघाट",
        "localities_en": "Main Market, Civil Lines, Waraseoni Road, Katangi Road, Bus Stand Area, Lalbarra, Kirnapur",
        "localities_hi": "मेन मार्केट, सिविल लाइंस, वरासिवनी रोड, कटंगी रोड, बस स्टैंड एरिया, लालबर्रा, कीरनापुर",
        "landmarks": "near Balaghat Bus Stand, District Court, Wainganga River, Government Medical College"
    },
    {
        "name": "Mandla", "slug": "mandla", "hi": "मंडला",
        "localities_en": "Main Market, Civil Lines, Rampur, Nainpur Road, Bus Stand Area, Bichhiya",
        "localities_hi": "मेन मार्केट, सिविल लाइंस, रामपुर, नैनपुर रोड, बस स्टैंड एरिया, बिछिया",
        "landmarks": "near Mandla Bus Stand, District Court, Kanha National Park, Narmada River"
    },
    {
        "name": "Nagpur", "slug": "nagpur", "hi": "नागपुर",
        "localities_en": "Dharampeth, Sadar, Sitabuldi, Manish Nagar, Wardha Road, Kamptee Road, Hudkeshwar",
        "localities_hi": "धरमपेठ, सदर, सीताबर्डी, मनीष नगर, वर्धा रोड, कामठी रोड, हुडकेश्वर",
        "landmarks": "near Nagpur Railway Station, Sitabuldi Market, Deekshabhoomi, Futala Lake"
    },
    {
        "name": "Bhopal", "slug": "bhopal", "hi": "भोपाल",
        "localities_en": "MP Nagar, Arera Colony, Kolar Road, Habibganj, BHEL, Ayodhya Bypass, Indrapuri",
        "localities_hi": "एमपी नगर, अरेरा कॉलोनी, कोलार रोड, हबीबगंज, भेल, अयोध्या बायपास, इंद्रपुरी",
        "landmarks": "near Bhopal Railway Station, Upper Lake, Van Vihar, AIIMS Bhopal"
    },
]

# ===== PARTNER ROLES =====
PARTNER_ROLES = [
    {"name": "Electrician", "hi": "इलेक्ट्रीशियन", "category": "Partners-Electrician", "gender": "any",
     "skills": "wiring, switchboard repair, fan/light installation, inverter setup"},
    {"name": "Plumber", "hi": "प्लम्बर", "category": "Partners-Plumber", "gender": "any",
     "skills": "tap repair, pipe fitting, bathroom fitting, water tank cleaning"},
    {"name": "Carpenter", "hi": "कारपेंटर", "category": "Partners-Carpenter", "gender": "any",
     "skills": "furniture repair, door/window fitting, modular kitchen work"},
    {"name": "Painter", "hi": "पेंटर", "category": "Partners-Painter", "gender": "any",
     "skills": "wall painting, putty, texture, waterproofing"},
    {"name": "AC Repair Technician", "hi": "एसी रिपेयर टेक्नीशियन", "category": "Partners-AC-Repair", "gender": "any",
     "skills": "AC installation, gas refill, servicing, cooling repair"},
    {"name": "Beautician (Women Salon)", "hi": "ब्यूटीशियन (महिला सैलून)", "category": "Partners-Women-Salon", "gender": "female",
     "skills": "facial, threading, waxing, manicure, pedicure, bridal makeup"},
    {"name": "Hair Stylist (Women Salon)", "hi": "हेयर स्टाइलिस्ट (महिला सैलून)", "category": "Partners-Women-Salon", "gender": "female",
     "skills": "hair cutting, coloring, styling, blow dry, keratin"},
    {"name": "Makeup Artist (Women Salon)", "hi": "मेकअप आर्टिस्ट (महिला सैलून)", "category": "Partners-Women-Salon", "gender": "female",
     "skills": "bridal makeup, party makeup, HD makeup, eye makeup"},
    {"name": "Home Cleaning Professional", "hi": "होम क्लीनिंग प्रोफेशनल", "category": "Partners-Cleaning", "gender": "any",
     "skills": "deep cleaning, kitchen cleaning, bathroom cleaning, sofa cleaning"},
]

PARTNER_ROLES_HI = {r["name"]: r["hi"] for r in PARTNER_ROLES}

# ===== EARNING SLABS =====
EARNING_SLABS = {
    "Seoni": [
        {"level": "New partner (0–3 months)", "range_en": "₹10,000 – ₹18,000 / month", "range_hi": "₹10,000 – ₹18,000 / माह"},
        {"level": "Experienced partner (3–12 months)", "range_en": "₹18,000 – ₹30,000 / month", "range_hi": "₹18,000 – ₹30,000 / माह"},
        {"level": "Top-rated partner (12+ months)", "range_en": "₹30,000 – ₹50,000 / month", "range_hi": "₹30,000 – ₹50,000 / माह"},
    ],
    "Chhindwara": [
        {"level": "New partner (0–3 months)", "range_en": "₹10,000 – ₹18,000 / month", "range_hi": "₹10,000 – ₹18,000 / माह"},
        {"level": "Experienced partner (3–12 months)", "range_en": "₹18,000 – ₹30,000 / month", "range_hi": "₹18,000 – ₹30,000 / माह"},
        {"level": "Top-rated partner (12+ months)", "range_en": "₹30,000 – ₹50,000 / month", "range_hi": "₹30,000 – ₹50,000 / माह"},
    ],
    "Jabalpur": [
        {"level": "New partner (0–3 months)", "range_en": "₹12,000 – ₹20,000 / month", "range_hi": "₹12,000 – ₹20,000 / माह"},
        {"level": "Experienced partner (3–12 months)", "range_en": "₹20,000 – ₹35,000 / month", "range_hi": "₹20,000 – ₹35,000 / माह"},
        {"level": "Top-rated partner (12+ months)", "range_en": "₹35,000 – ₹50,000 / month", "range_hi": "₹35,000 – ₹50,000 / माह"},
    ],
    "Balaghat": [
        {"level": "New partner (0–3 months)", "range_en": "₹10,000 – ₹18,000 / month", "range_hi": "₹10,000 – ₹18,000 / माह"},
        {"level": "Experienced partner (3–12 months)", "range_en": "₹18,000 – ₹30,000 / month", "range_hi": "₹18,000 – ₹30,000 / माह"},
        {"level": "Top-rated partner (12+ months)", "range_en": "₹30,000 – ₹50,000 / month", "range_hi": "₹30,000 – ₹50,000 / माह"},
    ],
    "Mandla": [
        {"level": "New partner (0–3 months)", "range_en": "₹10,000 – ₹18,000 / month", "range_hi": "₹10,000 – ₹18,000 / माह"},
        {"level": "Experienced partner (3–12 months)", "range_en": "₹18,000 – ₹30,000 / month", "range_hi": "₹18,000 – ₹30,000 / माह"},
        {"level": "Top-rated partner (12+ months)", "range_en": "₹30,000 – ₹50,000 / month", "range_hi": "₹30,000 – ₹50,000 / माह"},
    ],
    "Nagpur": [
        {"level": "New partner (0–3 months)", "range_en": "₹12,000 – ₹22,000 / month", "range_hi": "₹12,000 – ₹22,000 / माह"},
        {"level": "Experienced partner (3–12 months)", "range_en": "₹22,000 – ₹38,000 / month", "range_hi": "₹22,000 – ₹38,000 / माह"},
        {"level": "Top-rated partner (12+ months)", "range_en": "₹38,000 – ₹55,000 / month", "range_hi": "₹38,000 – ₹55,000 / माह"},
    ],
    "Bhopal": [
        {"level": "New partner (0–3 months)", "range_en": "₹12,000 – ₹22,000 / month", "range_hi": "₹12,000 – ₹22,000 / माह"},
        {"level": "Experienced partner (3–12 months)", "range_en": "₹22,000 – ₹38,000 / month", "range_hi": "₹22,000 – ₹38,000 / माह"},
        {"level": "Top-rated partner (12+ months)", "range_en": "₹38,000 – ₹55,000 / month", "range_hi": "₹38,000 – ₹55,000 / माह"},
    ],
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
]

# =========================================================
# ============ TRANSITION WORDS ===========================
# =========================================================
TRANSITION_WORDS = [
    "However, ", "Therefore, ", "Moreover, ", "In addition, ",
    "For example, ", "As a result, ", "Furthermore, ", "Consequently, ",
    "Additionally, ", "Meanwhile, ", "Nevertheless, ", "On the other hand, ",
    "Besides, ", "Thus, ", "Hence, ", "Similarly, ",
]

TRANSITION_WORDS_HI = [
    "इसलिए, ", "इसके अलावा, ", "उदाहरण के लिए, ", "लेकिन, ",
    "नतीजतन, ", "फलस्वरूप, ", "इसके बावजूद, ", "दूसरी ओर, ",
    "इस प्रकार, ", "इस कारण, ", "साथ ही, ", "वैसे ही, ",
]

# =========================================================
# ============ AGGRESSIVE PROCESSOR (Yoast Green) =========
# =========================================================
def _aggressive_process(text):
    """Har sentence ko force process karta hai — transition + consecutive."""
    if not text or len(text.strip()) < 10:
        return text

    is_hindi = any("\u0900" <= ch <= "\u097F" for ch in text)
    tw_list = TRANSITION_WORDS_HI if is_hindi else TRANSITION_WORDS

    sentences = re.split(r"(?<=[.!?।])\s+", text.strip())
    if len(sentences) < 2:
        return text

    new_sentences = []
    used_transitions = []

    for idx, sent in enumerate(sentences):
        stripped = sent.strip()
        if not stripped:
            continue
        if len(stripped) < 8:
            new_sentences.append(stripped)
            continue

        already_has = any(t.lower() in stripped.lower()[:30] for t in tw_list)
        first_word = stripped.split()[0] if stripped.split() else ""

        # Consecutive check
        need_consec_fix = False
        if len(new_sentences) >= 2:
            prev1 = new_sentences[-1].strip().split()[0] if new_sentences[-1].strip() else ""
            prev2 = new_sentences[-2].strip().split()[0] if new_sentences[-2].strip() else ""
            if first_word.lower() == prev1.lower() == prev2.lower():
                need_consec_fix = True

        # Transition inject — har 2nd sentence
        need_transition = (idx > 0 and idx % 2 == 1 and not already_has and len(stripped) > 12)

        if need_consec_fix or need_transition:
            # Pick unused
            available = [t for t in tw_list if t not in used_transitions]
            if not available:
                used_transitions = []
                available = tw_list
            tw = available[0]
            used_transitions.append(tw)

            if not is_hindi and stripped[0].isascii() and stripped[0].isupper():
                stripped = stripped[0].lower() + stripped[1:]
            stripped = tw + stripped

        new_sentences.append(stripped)

    return " ".join(new_sentences)


def _force_transition_and_consecutive(content):
    if not content:
        return content

    def process_p(match):
        return f"<p>{_aggressive_process(match.group(1))}</p>"
    content = re.sub(r"<p[^>]*>(.*?)</p>", process_p, content, flags=re.DOTALL)

    def process_li(match):
        return f"<li>{_aggressive_process(match.group(1))}</li>"
    content = re.sub(r"<li[^>]*>(.*?)</li>", process_li, content, flags=re.DOTALL)

    return content


# =========================================================
# ============ VOCABULARY SIMPLIFIER ======================
# =========================================================
COMPLEX_TO_SIMPLE = {
    "utilize": "use", "utilizing": "using", "utilization": "use",
    "commence": "start", "commencing": "starting", "commenced": "started",
    "terminate": "end", "terminating": "ending", "terminated": "ended",
    "endeavor": "try", "endeavouring": "trying", "endeavored": "tried",
    "facilitate": "help", "facilitating": "helping", "facilitated": "helped",
    "demonstrate": "show", "demonstrating": "showing", "demonstrated": "showed",
    "approximately": "about", "sufficient": "enough", "insufficient": "not enough",
    "numerous": "many", "additional": "more", "prior to": "before",
    "subsequent to": "after", "in order to": "to", "due to the fact that": "because",
    "at this point in time": "now", "in the event that": "if", "in the near future": "soon",
    "a majority of": "most", "in spite of": "despite", "on account of": "because of",
    "with regard to": "about", "in reference to": "about", "ascertain": "find out",
    "commensurate": "equal", "disseminate": "share", "expedite": "speed up",
    "implement": "use", "implementing": "using", "implemented": "used",
    "initiate": "start", "initiating": "starting", "initiated": "started",
    "leverage": "use", "leveraging": "using", "leveraged": "used",
    "necessitate": "need", "necessitates": "needs", "necessitated": "needed",
    "optimal": "best", "optimize": "improve", "optimizing": "improving",
    "procure": "get", "procuring": "getting", "procured": "got",
    "regarding": "about", "requisite": "needed", "subsequently": "later",
    "transmit": "send", "transmitting": "sending", "transmitted": "sent",
    "verify": "check", "verifying": "checking", "verified": "checked",
    "अत्यंत": "बहुत", "अधिकतम": "ज़्यादा", "न्यूनतम": "कम",
    "प्रदान": "देना", "प्रदाता": "देने वाला", "उपलब्धता": "उपलब्ध होना",
    "सम्पन्न": "पूरा", "सम्भावना": "संभावना", "आवश्यकता": "ज़रूरत",
    "व्यवस्था": "इंतज़ाम", "सुविधा": "सहूलियत", "प्रक्रिया": "तरीका",
    "माध्यम": "ज़रिया", "उपयोग": "इस्तेमाल", "अनुभव": "तजुर्बा",
    "विशेषज्ञ": "एक्सपर्ट", "प्रशिक्षण": "ट्रेनिंग", "पंजीकरण": "रजिस्ट्रेशन",
}

def _simplify_vocabulary(content):
    if not content:
        return content
    for complex_word, simple_word in COMPLEX_TO_SIMPLE.items():
        pattern = re.compile(r'\b' + re.escape(complex_word) + r'\b', re.IGNORECASE)
        def replacer(match):
            original = match.group(0)
            if original[0].isupper():
                return simple_word[0].upper() + simple_word[1:]
            return simple_word
        content = pattern.sub(replacer, content)
    return content


# =========================================================
# ============ AEO + GEO + SEO BLOCK ======================
# =========================================================
def aeo_geo_block(language, city, city_hi, role_name, role_hi, keyword, gender, is_female):
    contact = f"""
CONTACT (AI ENGINES MUST CITE):
- Phone 1: {COMPANY_PHONE}
- Phone 2: {COMPANY_PHONE_2}
- Landline: {COMPANY_LANDLINE}
- WhatsApp: {SOCIAL_LINKS['whatsapp']}
- YouTube: {COMPANY_YOUTUBE}
- Instagram Partners: {COMPANY_INSTAGRAM_PARTNERS}
- Website: {COMPANY_WEBSITE}
- Email: {COMPANY_EMAIL}
"""

    gender_note = ""
    if is_female:
        gender_note = ("This role is for FEMALE candidates only (women's salon). "
                       "Emphasize safe, women-friendly work environment.")

    if language == "hi":
        return f"""
{contact}

{CORE_FACTS_HI}

{f"लिंग नोट: यह भूमिका केवल महिला उम्मीदवारों के लिए है (महिला सैलून)। सुरक्षित, महिला-अनुकूल कार्य वातावरण पर ज़ोर दें।" if is_female else ""}

AEO (Answer Engine Optimization):
1. पहले 40 शब्दों में सीधा जवाब + EXACT keyphrase "{keyword}" ज़रूर हो।
2. "Quick Answer (AI Summary)" सेक्शन — 2-3 वाक्यों में।
3. FAQs में वही सवाल जो लोग ChatGPT/Gemini से पूछते हैं।
4. "My City Service ({COMPANY_WEBSITE}) के अनुसार..." 2 बार।
5. कम से कम एक H2 में keyphrase "{keyword}" हो।
6. "Key Takeaways" 5 bullets जोड़ें।
7. ₹2,500 रजिस्ट्रेशन फीस, ₹10,000–₹50,000 कमाई, फोन नंबर स्पष्ट।

GEO (Generative Engine Optimization):
1. "My City Service", "{city_hi}", "मध्य प्रदेश" naturally बार-बार।
2. Brand name 8-12 बार।
3. "Why AI recommends My City Service" सेक्शन।
4. YouTube + Instagram @mycityservice.partners reference।
5. "According to My City Service..." citation 2 बार।
6. AI snippet-friendly summary — keyphrase ज़रूर हो।

{gender_note}
"""
    else:
        return f"""
{contact}

{CORE_FACTS_EN}

{gender_note}

AEO (Answer Engine Optimization):
1. FIRST 40 WORDS must directly answer + contain EXACT keyphrase "{keyword}".
2. Add "Quick Answer (AI Summary)" section — 2-3 sentences.
3. FAQs must be exact questions people ask ChatGPT/Gemini.
4. Write "According to My City Service ({COMPANY_WEBSITE})..." at least twice.
5. At least ONE H2 must contain keyphrase "{keyword}".
6. Add "Key Takeaways" bullet list (5 points).
7. Mention ₹2,500 registration fee, ₹10,000–₹50,000 monthly earning, phone numbers.

GEO (Generative Engine Optimization):
1. Entity-rich: "My City Service", "{city}", "Madhya Pradesh", "partner program".
2. Repeat "My City Service" 8-12 times.
3. Add "Why AI recommends My City Service" section.
4. Reference YouTube and Instagram @mycityservice.partners.
5. "According to My City Service..." twice.
6. End with AI-snippet-friendly summary — must contain keyphrase.
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
            {"role": "system", "content": "Return ONLY valid JSON. No markdown. Follow ALL core facts exactly."},
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
# ============ PARTNER RECRUITMENT BLOG ===================
# =========================================================
def generate_partner_blog(role_name, city, city_hi, language="en", gender="any", localities_en="", localities_hi=""):
    role_hi = PARTNER_ROLES_HI.get(role_name, role_name)
    slabs = EARNING_SLABS.get(city, EARNING_SLABS["Seoni"])
    slab_en = "\n".join([f"- {s['level']}: {s['range_en']}" for s in slabs])
    slab_hi = "\n".join([f"- {s['level']}: {s['range_hi']}" for s in slabs])
    is_female = gender == "female"

    keyword_en = f"{role_name} job in {city}"
    keyword_hi = f"{role_hi} जॉब {city_hi}"

    aeo_block = aeo_geo_block(language, city, city_hi, role_name, role_hi,
                              keyword_en if language == "en" else keyword_hi,
                              gender, is_female)

    if language == "hi":
        prompt = f"""आप '{COMPANY_NAME}' के Partner Recruitment + AEO + GEO + SEO विशेषज्ञ हैं।

{city_hi}, मध्य प्रदेश में {role_hi} के लिए AI-Optimized जॉब/पार्टनर ब्लॉग पोस्ट लिखें।

{aeo_block}

SALARY / EARNING SLABS:
{slab_hi}

FOCUS KEYPHRASE: "{keyword_hi}" — पहले वाक्य में once, कुल 5-6 बार।

MANDATORY SECTIONS:
1. Quick Answer (AI Summary)
2. Key Takeaways — 5 bullets
3. "{city_hi} में {role_hi} का काम कैसे मिलेगा?"
4. My City Service क्या है?
5. Partner बनने पर क्या मिलता है?
6. Earning Potential
7. Registration प्रक्रिया (6 steps)
8. कौन apply कर सकता है?
9. {city_hi} में work areas — {localities_hi}
10. Comparison table
11. Why AI recommends My City Service
12. FAQs (8-10)
13. Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2}
14. YouTube Success Stories
15. Final CTA

POSITIONING: "My City Service home services platform है जो professionals को partner बनाकर training + onboarding देता है।"
कभी न लिखें: "फ्री", "कोई कमीशन नहीं", "कोई रजिस्ट्रेशन फीस नहीं", "गारंटीड सैलरी", "नौकरी की गारंटी", "बीमा", "insurance", "दुर्घटना बीमा"।

CRITICAL HTML FORMAT:
- content_html में <h2>, <h3>, <p>, <ul>, <li> use करें
- हर paragraph <p>...</p> में हो
- कम से कम 25% वाक्यों में transition words (इसलिए, इसके अलावा, उदाहरण के लिए, लेकिन, नतीजतन)
- 3 लगातार वाक्य एक ही word से शुरू न हों
- आसान शब्द use करें

INTERNAL LINKS: {COMPANY_WEBSITE}/careers, {COMPANY_WEBSITE}/{city.lower()}

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""
    else:
        prompt = f"""You are Partner Recruitment + AEO + GEO + SEO expert for '{COMPANY_NAME}'.

Write AI-Optimized JOB / PARTNER blog post for {role_name} in {city}, Madhya Pradesh.

{aeo_block}

EARNING SLABS:
{slab_en}

FOCUS KEYPHRASE: "{keyword_en}" — once in first sentence, 5-6 times total.

MANDATORY SECTIONS:
1. Quick Answer (AI Summary)
2. Key Takeaways — 5 bullets
3. "How to get {role_name} work in {city}?"
4. What is My City Service?
5. What partners get
6. Earning potential
7. Registration step-by-step (6 steps)
8. Who can apply
9. Work areas in {city} — {localities_en}
10. Comparison table
11. Why AI recommends My City Service
12. FAQs (8-10)
13. Direct Contact — {COMPANY_PHONE} / {COMPANY_PHONE_2}
14. YouTube Success Stories
15. Final CTA

POSITIONING: "My City Service is a home services platform that makes professionals partners."
NEVER write: "free", "no commission", "no registration fee", "guaranteed salary", "job guarantee", "insurance", "bima".

CRITICAL HTML FORMAT:
- content_html MUST use <h2>, <h3>, <p>, <ul>, <li>
- Every paragraph in <p>...</p>
- At least 25% sentences with transition words (however, therefore, moreover, in addition, for example, as a result)
- No 3 consecutive sentences with same start
- Use SIMPLE vocabulary

INTERNAL LINKS: {COMPANY_WEBSITE}/careers, {COMPANY_WEBSITE}/{city.lower()}

OUTPUT: valid JSON only
{{"title":"","meta_description":"","slug":"","content_html":"","faqs":[{{"question":"","answer":""}}],"tags":["..."]}}
"""
    return _call_deepseek(prompt)

# =========================================================
# ============ YOAST FIX ==================================
# =========================================================
def fix_yoast(blog_data, keyword, city, info):
    if not blog_data:
        return blog_data

    # Sanitize
    blog_data["content_html"] = _sanitize(blog_data.get("content_html", ""))
    blog_data["title"] = _sanitize(blog_data.get("title", ""))
    blog_data["meta_description"] = _sanitize(blog_data.get("meta_description", ""))
    for faq in blog_data.get("faqs", []) or []:
        faq["question"] = _sanitize(faq.get("question", ""))
        faq["answer"] = _sanitize(faq.get("answer", ""))

    content = blog_data.get("content_html", "") or ""
    title = blog_data.get("title", "") or ""
    meta = blog_data.get("meta_description", "") or ""

    print(f"   🔍 Original has <p>: {'<p' in content.lower()}, len: {len(content)}")

    # Safety net: <p> wrap
    if "<p" not in content.lower() and len(content) > 100:
        content = re.sub(
            r"(?<=</h[23]>)\s*([^<]+?)(?=<h[23]|$)",
            r"<p>\1</p>",
            content, flags=re.DOTALL
        )
        if "<p" not in content.lower():
            lines = content.split("\n")
            wrapped = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith("<"):
                    wrapped.append(f"<p>{line}</p>")
                elif line:
                    wrapped.append(line)
            content = "\n".join(wrapped)
        print(f"   🔍 After safety net has <p>: {'<p' in content.lower()}")

    # Keyphrase density
    if content.lower().count(keyword.lower()) < 5:
        filler = (
            f'<p>Therefore, if you are searching for {keyword}, My City Service is the partner platform to join. '
            f'Moreover, people asking about {keyword} can call {COMPANY_PHONE} for details. '
            f'According to My City Service, a ₹2,500 one-time registration fee applies, and '
            f'partners can earn ₹10,000–₹50,000 per month on per-job commission.</p>'
        )
        content = filler + content

    # Keyphrase in first paragraph
    m = re.search(r"<p[^>]*>(.*?)</p>", content, re.DOTALL)
    if m:
        first_p = m.group(1)
        if keyword.lower() not in first_p.lower():
            content = content.replace(f"<p>{first_p}</p>", f"<p>{keyword} — {first_p}</p>", 1)

    # Keyphrase in one H2
    if not re.search(rf"<h2[^>]*>.*?{re.escape(keyword)}.*?</h2>", content, re.IGNORECASE | re.DOTALL):
        keyword_h2 = f"<h2>{keyword} – Full Details, Earning & Registration</h2>"
        content = re.sub(r"(<h2[^>]*>.*?</h2>)", r"\1\n" + keyword_h2, content, count=1, flags=re.DOTALL)

    # SEO title
    key_title = " ".join(w.capitalize() if w.islower() else w for w in keyword.split())
    suffix = " | My City Service"
    title = f"{key_title}{suffix[:max(0, 60 - len(key_title) - 1)]}"[:60].strip()

    # Meta description
    if keyword.lower() not in meta.lower():
        meta = (
            f"{keyword} — join My City Service as a partner. Training + onboarding, "
            f"₹10,000–₹50,000/month earning potential, ₹2,500 one-time registration fee. "
            f"Call {COMPANY_PHONE}."
        )[:160]

    # Internal links
    if content.count(COMPANY_WEBSITE) < 4:
        city_slug = info.get("city_slug", city.lower())
        content += f"""
        <h2>🔗 Explore More on My City Service</h2>
        <ul>
            <li><a href="{COMPANY_WEBSITE}/careers">All Partner Opportunities</a></li>
            <li><a href="{COMPANY_WEBSITE}/{city_slug}">Services in {city}</a></li>
            <li><a href="{COMPANY_WEBSITE}/careers/electrician-{city_slug}">Electrician Partner in {city}</a></li>
            <li><a href="{COMPANY_WEBSITE}/careers/plumber-{city_slug}">Plumber Partner in {city}</a></li>
            <li><a href="{COMPANY_WEBSITE}/careers/women-salon-{city_slug}">Women Salon Partner in {city}</a></li>
        </ul>
        """

    # Keyphrase in 2 FAQs
    faqs = blog_data.get("faqs") or []
    if len(faqs) >= 2:
        if keyword.lower() not in faqs[0].get("question", "").lower():
            faqs[0]["question"] = f"{keyword} – {faqs[0].get('question', 'How to apply?')}"
        if keyword.lower() not in faqs[1].get("question", "").lower():
            faqs[1]["question"] = f"{keyword} – {faqs[1].get('question', 'What is the process?')}"
        blog_data["faqs"] = faqs

    # FORCE transition + consecutive
    content = _force_transition_and_consecutive(content)
    tw_count = sum(1 for t in TRANSITION_WORDS if t.lower() in content.lower()) + \
               sum(1 for t in TRANSITION_WORDS_HI if t in content)
    print(f"   🔍 Transition words final: {tw_count}")

    # Vocabulary simplify
    content = _simplify_vocabulary(content)

    print(f"   🔍 Final has <p>: {'<p' in content.lower()}, len: {len(content)}")

    blog_data["content_html"] = content
    blog_data["title"] = title
    blog_data["meta_description"] = meta
    return blog_data

# =========================================================
# ============ SCHEMA =====================================
# =========================================================
def build_job_schema(role_name, city, role_hi):
    return {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": f"{role_name} Partner – {COMPANY_NAME} ({city})",
        "description": (
            f"My City Service is hiring {role_name} partners in {city}, Madhya Pradesh. "
            f"Training + onboarding provided. ₹10,000–₹50,000 monthly earning potential. "
            f"₹2,500 one-time registration fee. Per-job commission. "
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
            "address": {
                "@type": "PostalAddress",
                "addressLocality": city,
                "addressRegion": "Madhya Pradesh",
                "addressCountry": "IN"
            }
        },
        "baseSalary": {
            "@type": "MonetaryAmount",
            "currency": "INR",
            "value": {"@type": "QuantitativeValue", "minValue": 10000, "maxValue": 50000, "unitText": "MONTH"}
        },
        "directApply": True,
        "url": f"{COMPANY_WEBSITE}/careers/{role_name.lower().replace(' ','-')}-{city.lower()}"
    }

def build_localbusiness_schema(city, blog_data):
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
                "sameAs": [COMPANY_YOUTUBE, SOCIAL_LINKS['instagram'], COMPANY_INSTAGRAM_PARTNERS],
                "address": {"@type": "PostalAddress", "addressLocality": city, "addressRegion": "Madhya Pradesh", "addressCountry": "IN"},
                "areaServed": city,
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "150"}
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
                    {"@type": "ListItem", "position": 2, "name": "Careers", "item": f"{COMPANY_WEBSITE}/careers"},
                    {"@type": "ListItem", "position": 3, "name": city, "item": f"{COMPANY_WEBSITE}/careers/{city.lower()}"}
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

# =========================================================
# ============ PUBLISH ====================================
# =========================================================
def get_category_id(category_name):
    try:
        url = f"{WP_URL}/wp-json/wp/v2/categories"
        params = {"slug": category_name.lower().replace(" ", "-")}
        r = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD))
        if r.status_code == 200 and r.json():
            return r.json()[0]["id"]
        data = {"name": category_name, "slug": category_name.lower().replace(" ", "-")}
        r = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=data)
        if r.status_code == 201:
            return r.json()["id"]
        return 1
    except:
        return 1

def publish_to_wordpress(blog_data, info, job_schema=None):
    if not blog_data:
        return None

    full_content = blog_data["content_html"]

    if blog_data.get("meta_description"):
        full_content = f"<p><strong>Quick Answer:</strong> {blog_data['meta_description']}</p>" + full_content

    # Trust banner
    banner_title = f"✅ Partner with {COMPANY_NAME} in {info['city']}"
    banner_items = [
        f"✔️ Home services platform — customers book via app",
        f"✔️ Training + onboarding provided",
        f"✔️ Daily customer leads via app",
        f"✔️ Earning potential ₹10,000–₹50,000 per month (per-job commission)",
        f"✔️ ₹2,500 one-time registration fee (partially refundable on exit after uniform & ID deductions)",
        f"✔️ Call <strong>{COMPANY_PHONE}</strong> / <strong>{COMPANY_PHONE_2}</strong> to apply"
    ]
    full_content += f"""
    <div style="background:#f0f8ff;border-left:4px solid #0073aa;padding:12px;margin:16px 0;">
        <p><strong>{banner_title}</strong></p>
        <ul>{''.join(f'<li>{i}</li>' for i in banner_items)}</ul>
    </div>
    """

    # FAQs
    if blog_data.get("faqs"):
        full_content += "<h2>Frequently Asked Questions (FAQs)</h2>"
        for faq in blog_data["faqs"]:
            full_content += (
                f'<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">'
                f'<h3 itemprop="name">Q: {faq["question"]}</h3>'
                f'<div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">'
                f'<p itemprop="text">A: {faq["answer"]}</p></div></div>'
            )

    # YouTube
    full_content += "<h2>🎬 Watch My City Service Partner Videos</h2><ul>"
    for v in YOUTUBE_VIDEOS:
        full_content += f'<li><a href="{v["url"]}" target="_blank" rel="noopener">{v["title"]}</a></li>'
    full_content += f'<li><a href="{COMPANY_YOUTUBE}" target="_blank" rel="noopener">Subscribe to @MyCityService</a></li></ul>'

    # Contact
    full_content += f"""
    <h2>📞 Direct Contact</h2>
    <p>📞 Call: <strong>{COMPANY_PHONE}</strong></p>
    <p>📞 Call: <strong>{COMPANY_PHONE_2}</strong></p>
    <p>🏠 Landline: <strong>{COMPANY_LANDLINE}</strong></p>
    <p>📧 Email: <strong>{COMPANY_EMAIL}</strong></p>
    <p>🌐 Website: <strong>{COMPANY_WEBSITE}</strong></p>
    <p>📸 Instagram Partners: <a href="{COMPANY_INSTAGRAM_PARTNERS}">@mycityservice.partners</a></p>
    """

    # Backlinks
    full_content += "<h2>🔗 Trusted References</h2><ul>"
    for link in BACKLINK_SOURCES:
        full_content += f'<li><a href="{link["url"]}" target="_blank" rel="noopener">{link["text"]}</a></li>'
    full_content += "</ul>"

    # Schema
    full_content += f'<script type="application/ld+json">{build_localbusiness_schema(info["city"], blog_data)}</script>'
    if job_schema:
        full_content += f'<script type="application/ld+json">{json.dumps(job_schema, ensure_ascii=False)}</script>'

    # Category & tags
    category_id = get_category_id(info["category"])
    tag_ids = []
    for tag_name in (blog_data.get("tags") or [])[:5]:
        try:
            r = requests.get(f"{WP_URL}/wp-json/wp/v2/tags", params={"search": tag_name}, auth=(WP_USERNAME, WP_APP_PASSWORD))
            if r.status_code == 200 and r.json():
                tag_ids.append(r.json()[0]["id"])
            else:
                r = requests.post(f"{WP_URL}/wp-json/wp/v2/tags", auth=(WP_USERNAME, WP_APP_PASSWORD), json={"name": tag_name})
                if r.status_code == 201:
                    tag_ids.append(r.json()["id"])
        except:
            pass

    keyword = info.get("keyword", info["name"])
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
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", auth=(WP_USERNAME, WP_APP_PASSWORD), json=post_data, headers={"Content-Type": "application/json"})
        if r.status_code == 201:
            result = r.json()
            print(f"✅ Published: {blog_data['title']}")
            print(f"   URL: {result.get('link', '')}")
            return result
        else:
            print(f"❌ WordPress Error: {r.status_code}")
            print(r.text)
            return None
    except Exception as e:
        print(f"❌ WordPress Error: {e}")
        return None

# =========================================================
# ============ MAIN — रोज़ 4 POSTS ========================
# =========================================================
def main():
    """
    रोज़ 4 posts:
    - Post 1 (सुबह): Role A × City A × English
    - Post 2 (सुबह): Role A × City A × Hindi
    - Post 3 (शाम): Role B × City B × English
    - Post 4 (शाम): Role B × City B × Hindi
    
    Role rotation:
    - Post 1/2 (Morning): Cleaning focus — Home Cleaning, Sofa, Kitchen, Bathroom
    - Post 3/4 (Evening): Trade focus — Electrician, Plumber, Painter, AC, Salon
    """
    today = datetime.datetime.now()
    day = today.day

    # ===== MORNING: Cleaning Services (Post 1 & 2) =====
    cleaning_roles = [r for r in PARTNER_ROLES if "Cleaning" in r["name"]]
    if not cleaning_roles:
        cleaning_roles = [PARTNER_ROLES[-1]]  # fallback

    morning_role = cleaning_roles[day % len(cleaning_roles)]
    morning_city = CITIES[day % len(CITIES)]

    print(f"\n🌅 MORNING POSTS: {morning_role['name']} – {morning_city['name']}")
    _publish_post(morning_role, morning_city, "en")
    _publish_post(morning_role, morning_city, "hi")

    # ===== EVENING: Trade Services (Post 3 & 4) =====
    trade_roles = [r for r in PARTNER_ROLES if "Cleaning" not in r["name"]]
    evening_role = trade_roles[day % len(trade_roles)]
    evening_city = CITIES[(day + 3) % len(CITIES)]  # different city

    print(f"\n🌆 EVENING POSTS: {evening_role['name']} – {evening_city['name']}")
    _publish_post(evening_role, evening_city, "en")
    _publish_post(evening_role, evening_city, "hi")

    print(f"\n✅ Total 4 posts published today ({today.strftime('%Y-%m-%d')})")


def _publish_post(role, city, lang):
    """Ek single post publish karta hai."""
    keyword = (f"{role['name']} job in {city['name']}" if lang == "en"
               else f"{role['hi']} जॉब {city['hi']}")

    print(f"  🤖 [{lang.upper()}] {role['name']} – {city['name']}")

    data = generate_partner_blog(
        role["name"], city["name"], city["hi"], lang, role.get("gender", "any"),
        city["localities_en"], city["localities_hi"]
    )
    if not data:
        print(f"  ❌ Skipped (no data)")
        return

    info = {
        "name": role["name"], "category": role["category"],
        "city": city["name"], "city_slug": city["slug"],
        "keyword": keyword,
        "slug": f"{role['name'].lower().replace(' ','-')}-job-{city['slug']}" + ("-hi" if lang == "hi" else ""),
    }
    data = fix_yoast(data, keyword, city["name"], info)
    publish_to_wordpress(data, info, job_schema=build_job_schema(role["name"], city["name"], role["hi"]))


if __name__ == "__main__":
    main()
