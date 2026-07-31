import os
import json
import requests
import datetime

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

SERVICES = [
    {"name": "Electrician", "category": "Electrician"},
    {"name": "AC Repair", "category": "AC-Service"},
    {"name": "Plumber", "category": "Plumber"},
    {"name": "Home Cleaning", "category": "Cleaning-Services"},
    {"name": "Appliance Repair", "category": "Appliance-Repair"},
    {"name": "Carpenter", "category": "Carpenter"},
    {"name": "Painting", "category": "Painting-Services"},
    {"name": "Water Purifier", "category": "Water-Purifier"}
]

def get_category_id(category_name):
    """WordPress में category ID fetch करें"""
    try:
        url = f"{WP_URL}/wp-json/wp/v2/categories"
        params = {"slug": category_name.lower().replace(" ", "-")}
        response = requests.get(url, params=params, auth=(WP_USERNAME, WP_APP_PASSWORD))
        
        if response.status_code == 200 and response.json():
            return response.json()[0]["id"]
        
        # Category नहीं है तो create करें
        data = {"name": category_name, "slug": category_name.lower().replace(" ", "-")}
        response = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=data)
        if response.status_code == 201:
            return response.json()["id"]
        return 1  # Default: Uncategorized
    except:
        return 1

def generate_blog_post(service_name):
    prompt = f"""You are an expert Senior SEO, GEO, and Local Content Strategist for 'seoniservice.in'.

Write a comprehensive SEO-optimized blog post about {service_name} services in Seoni, MP.

STRUCTURE MUST INCLUDE:
1. SEO Metadata: Catchy title (under 60 chars), meta description (under 160 chars with CTA), SEO-friendly slug
2. Introduction with local Seoni intent
3. Why Choose My City Service (seoniservice.in)
4. Comprehensive Service Overview
5. Pricing & Process
6. Tools, Safety & Maintenance
7. Local Service Areas: Main Road, Subhash Ward, Barapatthar
8. FAQs (5-7 questions with answers)
9. Strong Call to Action
10. Social Media Promotion Pack

IMPORTANT: Make content readable with proper H2, H3 headings, short paragraphs, and bullet points.

OUTPUT FORMAT: Return valid JSON only:
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "content_html": "<full HTML content with proper headings>",
    "faqs": [{{"question": "", "answer": ""}}],
    "tags": ["keyword1", "keyword2", "keyword3"]
}}
"""

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": "Return valid JSON only."}, {"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4000
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

    # Content build
    full_content = blog_data["content_html"]
    if blog_data.get("faqs"):
        faq_html = "<h2>Frequently Asked Questions</h2>"
        for faq in blog_data["faqs"]:
            faq_html += f"<h3>Q: {faq['question']}</h3><p>A: {faq['answer']}</p>"
        full_content += faq_html

    # Category ID get करें
    category_id = get_category_id(service_info["category"])

    # Tags create/attach करें
    tag_ids = []
    if blog_data.get("tags"):
        for tag_name in blog_data["tags"][:5]:  # Max 5 tags
            tag_id = get_or_create_tag(tag_name)
            if tag_id:
                tag_ids.append(tag_id)

    # WordPress Post Data
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
    """Tag create या get करें"""
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
    service_info = SERVICES[day_index]
    service_name = service_info["name"]
    
    print(f"🤖 Generating blog for: {service_name}")
    blog_data = generate_blog_post(service_name)
    if blog_data:
        publish_to_wordpress(blog_data, service_info)

if __name__ == "__main__":
    main()
