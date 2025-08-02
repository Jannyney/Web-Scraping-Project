import requests
from bs4 import BeautifulSoup
import json
import time

SITEMAP_URL = "https://medium.com/sitemap/sitemap.xml"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
MAX_ARTICLES = 50  # Limit to 50 articles

# Function to fetch and parse sitemap XML to extract sub-sitemap links
def get_sitemap_links(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "xml")
    return [loc.get_text() for loc in soup.find_all("loc")]

# Function to extract article URLs from sub-sitemap with a limit
def get_article_links(sub_sitemap_url, max_links):
    response = requests.get(sub_sitemap_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "xml")
    article_links = [loc.get_text() for loc in soup.find_all("loc")]
    return article_links[:max_links]

# Function to scrape title, content, date, and author from Medium article
def scrape_medium_article(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return {"url": url, "error": "Failed to retrieve the page"}

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract title
    title = soup.find("title").text if soup.find("title") else "No title found"
    
    # Extract publication date
    date_meta = soup.find("meta", {"property": "article:published_time"})
    date = date_meta["content"] if date_meta else "No date found"
    
    # Extract author
    author_meta = soup.find("meta", {"name": "author"})
    author = author_meta["content"] if author_meta else "No author found"
    
    # Extract content (try to get all paragraphs)
    paragraphs = soup.find_all("p")
    content = "\n".join([p.text for p in paragraphs])  # Get all paragraphs
    
    # Limit content to 1000 characters for brevity in the result
    return {"url": url, "title": title, "date": date, "author": author, "content": content[:2000]}  # Increase content length

# Main function
def main():
    sitemap_links = get_sitemap_links(SITEMAP_URL)
    article_links = []
    
    for sub_sitemap in sitemap_links:
        if "posts" in sub_sitemap:  # Focus on article sitemaps
            time.sleep(2)  # Respect crawl delay
            new_links = get_article_links(sub_sitemap, MAX_ARTICLES - len(article_links))
            article_links.extend(new_links)
            
            if len(article_links) >= MAX_ARTICLES:
                break  # Stop once we reach 50 articles

    # Scrape all article URLs and store the results
    scraped_data = [scrape_medium_article(url) for url in article_links]
    
    # Save results to a JSON file
    with open("medium_articles.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
    
    print(f"Scraping completed. Extracted {len(scraped_data)} articles. Data saved to medium_articles.json")

if __name__ == "__main__":
    main()
