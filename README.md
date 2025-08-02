# Web Scraping Project: Medium Articles

## Web Resource Description

### Main URL:
**Main URL**:  
[https://medium.com](https://medium.com)  
Medium is a popular online publishing platform where people share articles on various topics such as technology, business, and lifestyle.

The main URL for the sitemap of Medium articles is:  
**https://medium.com/sitemap/sitemap.xml**

This URL provides the sitemap, which lists all the sub-sitemaps, leading to individual articles on Medium.

### Extracted Information:
From each article URL, the following information is extracted:
- **Url**: The url of the articles
- **Title**: The title of the article (from the `<title>` tag).
- **Publication Date**: The publication date of the article (from the `<meta property="article:published_time">` tag).
- **Author**: The author's name (from the `<meta name="author">` tag).
- **Content**: The main content of the article, which is extracted by scraping the text of the first few paragraphs (up to 2000 characters for brevity).

## Possible Issues with Crawling on Medium


### 1. Robot Exclusion Protocol (robots.txt)
Medium may block crawlers from accessing certain pages through the `robots.txt` file. It is essential to review Medium's `robots.txt` file before scraping to ensure compliance. Ignoring these rules could result in legal violations or blocked access to key content. Medium's `robots.txt` file is available at [https://medium.com/robots.txt](https://medium.com/robots.txt).

### 2. Availability of Sitemaps
Medium provides a sitemap at [https://medium.com/sitemap/sitemap.xml](https://medium.com/sitemap/sitemap.xml), which lists sub-sitemaps containing article URLs. However, the sitemap may be incomplete or outdated. If the sitemap is not properly maintained, the crawler might miss articles or take longer to scrape content, as it would have to find article URLs manually.

### 3. Rate Limiting and CAPTCHAs
Medium might implement rate limiting to prevent abuse. If the crawler sends too many requests in a short period, it could be blocked. Additionally, Medium may deploy CAPTCHA challenges to prevent automated access. These challenges can disrupt the crawling process and complicate the extraction of data. To avoid this, it is recommended to introduce delays between requests and consider handling CAPTCHAs if they appear.

### 4. Dynamic Content
Medium might load some content dynamically using JavaScript, which could be missed by traditional HTML parsers like BeautifulSoup. This means that scraping the full content may require additional tools, such as Selenium or Scrapy's Splash, to handle JavaScript rendering and ensure that the crawler can access and extract all the data, including dynamically loaded elements.
r HTML structure. If Medium alters the layout, the scraper may break or stop functioning.

## Design of the Extraction Task

### Inputs:
- **Sitemap URL**: The initial sitemap URL (`https://medium.com/sitemap/sitemap.xml`) which lists all the sub-sitemaps containing the article URLs.
- **Article URLs**: Extracted from the sitemap, used as input to scrape the individual articles.

### Outputs:
- **Structured Data**: A JSON file containing the extracted data from each article, with the following structure:
  ```json
  [
    {
      "url": "https://medium.com/article-link",
      "title": "Article Title",
      "date": "2024-03-12",
      "author": "Author Name",
      "content": "Article content here..."
    }
    
  ]
   ```

# Crawling Workflow

### Step 1: Checking robots.txt

Before scraping any website, especially a popular one like Medium, it's important to respect their crawling policies. Here's how you should approach it:

1.  **Access the robots.txt File**:Start by visiting the robots.txt file of the website:
    
    *   URL: https://medium.com/robots.txt
        
2.  textCopyEditUser-agent: \*Disallow: /It means that crawling is not allowed on any part of the website, and you should **not** proceed with scraping. If there is no restriction (or if it only restricts specific sections), you may proceed.
    
3.  **Handling Disallowed Access**:If crawling is disallowed, you should either:
    
    *   **Request Permission**: Contact the website owners for permission to scrape their data.
        
    *   **Look for Alternatives**: Some websites offer public APIs to fetch data in a structured way. Medium provides an API for certain data retrieval that you could use instead of scraping.
        

### Step 2: Fetching the Sitemap

Once robots.txt confirms crawling is allowed, the next step is to get the sitemap (https://medium.com/sitemap/sitemap.xml) and extract the sub-sitemaps that list article URLs.

### Step 3: Extracting Article URLs

From each sub-sitemap, extract URLs pointing to the individual articles. You can limit the number of articles to scrape (e.g., 50 articles) to ensure you're not overwhelming the server or scraping unnecessary data.

### Step 4: Scraping Content

For each article URL, fetch the page content, extract the title, author, publication date, and main content. You can use BeautifulSoup to parse and extract the necessary HTML elements. Limit the content extraction to prevent large data payloads.

### Step 5: Storing Data

Once the content is extracted, store the information in a structured JSON file to maintain the data in an easily usable format.
 ```json [

{

"url": "https://medium.com/article-link",

"title": "Article Title",

"date": "2024-03-12",

"author": "Author Name",

"content": "Article content here..."

}

```

### Issues During Design/Extraction:

1.  **Legal Constraints**: Medium’s robots.txt restricts web scraping, which could lead to blocking or legal issues. It's important to proceed cautiously and respect the site’s rules to avoid potential legal consequences.
    
2.  **Dynamic Content Loading**: Medium uses JavaScript to dynamically load certain content. Tools like BeautifulSoup won't be enough for these pages, and you might need tools like Selenium or Scrapy with Splash to handle content that loads after page load.
    
3.  **Rate Limiting and CAPTCHA**: Medium might impose rate limits or trigger CAPTCHA mechanisms if there are too many requests in a short period. This would slow down the scraping process or stop it altogether.
    
4.  **Changing HTML Structure**: Medium’s website design may change, affecting the consistency of data extraction. Frequent updates to scraping scripts are needed to adapt to these changes.
    
5.  **Data Completeness**: Missing data (like author, date, or tags) can occur, especially if content is dynamically loaded. Having backup mechanisms or fallbacks for incomplete data is essential.
    

### Ideas for Extensions/Improvements/Future Work:

1.  **Dynamic Content Handling**: Use Selenium, Scrapy with Splash, or Puppeteer to render JavaScript and fully extract content that is dynamically loaded. This would ensure better coverage of articles with JavaScript elements.
    
2.  **Proxy Rotation & Rate Limiting**: To handle the possibility of rate limiting or IP blocking, implement proxy rotation and slow down request frequency. Using a pool of proxies can help distribute the load and avoid detection.
    
3.  **Robust Error Handling**: Implement retry logic, error logging, and fallbacks for missing data to make the scraper more reliable. For instance, if one article doesn’t load, the scraper should continue with others.
    
4.  **Data Storage and Scalability**: Instead of saving to flat files, use a more scalable database like MongoDB or PostgreSQL for structured storage, better querying, and ease of data retrieval.
    
5.  **Data Enrichment**: Incorporate text analysis tools such as sentiment analysis, topic modeling, or keyword extraction to derive more insights from the mined data, making it more valuable.
    
6.  **Web Scraping Ethics & Legal Review**: Regularly audit the scraping process for compliance with Medium’s terms of service and legal considerations such as privacy laws (GDPR, etc.). This would ensure responsible scraping and reduce the risk of violations.
    
7.  **Handling Content Variations**: Since Medium articles can have varied structures (e.g., different article types, layouts, or nested elements), using a more flexible parsing approach (like XPath or CSS selectors) can help handle these variations better.
    
8.  **Data Visualization**: To make the mined data more insightful, integrate visualization tools (like Tableau or PowerBI) to display trends in article topics, author activity, or engagement metrics like comments and shares.
