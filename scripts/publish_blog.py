import os
import json
import requests
import datetime

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

SERVICES = ["Electrician", "AC Repair", "Plumber", "Home Cleaning", "Appliance Repair", "Carpenter", "Painting", "Water Purifier"]

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

OUTPUT FORMAT: Return valid JSON only:
{{
    "title": "",
    "meta_description": "",
    "slug": "",
    "content_html": "<full HTML content>",
    "faqs": [{{"question": "", "answer": ""}}]
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

def publish_to_wordpress(blog_data, service_name):
    if not blog_data:
        return None

    full_content = blog_data["content_html"]
    if blog_data.get("faqs"):
        faq_html = "<h2>Frequently Asked Questions</h2>"
        for faq in blog_data["faqs"]:
            faq_html += f"<h3>Q: {faq['question']}</h3><p>A: {faq['answer']}</p>"
        full_content += faq_html

    wp_api_url = f"{WP_URL}/wp-json/wp/v2/posts"
    post_data = {
        "title": blog_data["title"],
        "content": full_content,
        "status": "publish",
        "slug": blog_data["slug"],
        "meta": {
            "_yoast_wpseo_metadesc": blog_data["meta_description"],
            "_yoast_wpseo_title": blog_data["title"]
        }
    }

    try:
        response = requests.post(wp_api_url, auth=(WP_USERNAME, WP_APP_PASSWORD), json=post_data, headers={"Content-Type": "application/json"})
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Published: {blog_data['title']}")
            print(f"   URL: {result.get('link', '')}")
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
    service = SERVICES[day_index]
    print(f"🤖 Generating blog for: {service}")
    blog_data = generate_blog_post(service)
    if blog_data:
        publish_to_wordpress(blog_data, service)

if __name__ == "__main__":
    main()
