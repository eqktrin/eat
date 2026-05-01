from fastapi import APIRouter, Response
from datetime import datetime

router = APIRouter(tags=["SEO"])

@router.get("/robots.txt")
async def robots_txt():
    content = """User-agent: *
Allow: /
Disallow: /auth/
Disallow: /profile/
Disallow: /favorites/
Disallow: /orders/
Disallow: /allergens/

Sitemap: https://safeplate.ru/sitemap.xml
"""
    return Response(content=content, media_type="text/plain")

@router.get("/sitemap.xml")
async def sitemap_xml():
    today = datetime.now().strftime("%Y-%m-%d")
    
    pages = [
        {"url": "/", "priority": "1.0", "changefreq": "daily"},
        {"url": "/menu", "priority": "0.9", "changefreq": "daily"},
    ]
    
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        sitemap += f"""  <url>
    <loc>https://safeplate.ru{page["url"]}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{page["changefreq"]}</changefreq>
    <priority>{page["priority"]}</priority>
  </url>\n"""
    
    sitemap += '</urlset>'
    return Response(content=sitemap, media_type="application/xml")