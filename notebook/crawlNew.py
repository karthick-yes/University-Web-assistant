import os
import re
import io
import asyncio
import urllib.request
from urllib.parse import urlparse, quote
from urllib.error import HTTPError, URLError
from collections import deque
from html.parser import HTMLParser
import pypdf
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

HTTP_URL_PATTERN = r'^http[s]*://.+'

def sanitize_filename(url):
    """
    Sanitize a URL to be used as a safe filename.
    Handles both URL encoding and OS-specific filename restrictions.
    """
    # First, URL encode the string
    sanitized = quote(url, safe='')
    # Replace any remaining invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', sanitized)
    # Ensure filename length is within limits (255 chars is a common limit)
    if len(sanitized) > 255:
        # Keep the first 200 chars and last 55 chars to preserve uniqueness
        sanitized = f"{sanitized[:200]}___{sanitized[-55:]}"
    return sanitized

def pdf_to_text(pdf_content):
    """Convert PDF bytes to text with proper error handling."""
    try:
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = pypdf.PdfReader(pdf_file)
        text_content = []
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text_content.append(extracted_text)
        return "\n\n--- Page Break ---\n\n".join(text_content)
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return ""

class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hyperlinks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])

def get_hyperlinks(url, headers=None):
    try:
        request = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                **(headers or {})
            }
        )
        with urllib.request.urlopen(request) as response:
            if not response.info().get('Content-Type', '').startswith("text/html"):
                return []
            html = response.read().decode('utf-8')
            parser = HyperlinkParser()
            parser.feed(html)
            return parser.hyperlinks
    except (HTTPError, URLError) as e:
        print(f"Error fetching {url}: {e}")
        return []
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return []

def get_domain_hyperlinks(local_domain, url, headers=None):
    clean_links = []
    for link in set(get_hyperlinks(url, headers)):
        clean_link = None
        if re.search(HTTP_URL_PATTERN, link):
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link
        else:
            if not link.startswith(("#", "mailto:", "tel:", "javascript:")):
                clean_link = f"https://{local_domain}/{link.lstrip('/')}"
        if clean_link and clean_link.endswith("/"):
            clean_link = clean_link[:-1]
        if clean_link:
            clean_links.append(clean_link)
    return list(set(clean_links))

def getAllurls(url, max_pages=None):
    local_domain = urlparse(url).netloc
    queue = deque([url])
    seen = set([url])
    seen_list = []
    pages_crawled = 0
    
    # Define headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    while queue and (max_pages is None or pages_crawled < max_pages):
        url = queue.pop()
        print(f"Found: {url}")
        try:
            # Pass headers to get_domain_hyperlinks
            for link in get_domain_hyperlinks(local_domain, url, headers=headers):
                if link not in seen:
                    queue.append(link)
                    seen.add(link)
                    seen_list.append(link)
            pages_crawled += 1
        except Exception as e:
            print(f"Error processing {url}: {e}")
    return seen_list

async def process_result(result, debug_mode=False):
    """Process crawled data and save to markdown with proper file handling."""
    local_domain = urlparse(result.url).netloc
    base_dir = f"markdown/{local_domain}"
    os.makedirs(base_dir, exist_ok=True)

    # Create a sanitized filename
    sanitized_filename = sanitize_filename(result.url)
    
    # Create file paths
    content_path = os.path.join(base_dir, f"{sanitized_filename}.md")
    
    # Add source URL tracking
    with open(os.path.join(base_dir, "source_mapping.csv"), 'a', encoding='utf-8') as f:
        f.write(f"{sanitized_filename}.md,{result.url}\n")

    # Write content
    try:
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(f"# Source: {result.url}\n\n")
            
            if result.pdf is not None:
                f.write(pdf_to_text(result.pdf.bytes))
            else:
                if debug_mode:
                    # Include both raw and fit content in the same file with clear separation
                    f.write("## Raw Content\n\n")
                    f.write(result.markdown_v2.raw_markdown)
                    f.write("\n\n---\n\n## Processed Content\n\n")
                    f.write(result.markdown_v2.fit_markdown)
                else:
                    # Only include the processed content
                    f.write(result.markdown_v2.fit_markdown)
                    
    except Exception as e:
        print(f"Error saving content for {result.url}: {str(e)}")

async def crawl_streaming(start_url, max_pages=None, debug_mode=False):
    """Main function to crawl pages asynchronously."""
    print(f"Starting crawl of {start_url}")
    urls = getAllurls(start_url, max_pages=max_pages)
    print(f"Found {len(urls)} URLs to process")

    md_generator = DefaultMarkdownGenerator(
        options={
            "citations": True,
            "escape_html": False,
            "skip_internal_links": True
        },
        content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
    )

    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        text_mode=True,
        user_agent_mode="random"
    )
    
    run_config = CrawlerRunConfig(word_count_threshold=10,
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator,
        pdf=True,
        excluded_tags=['form', 'header', 'footer', 'nav', 'section'],
        exclude_external_links=True,
        exclude_social_media_links=True,)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(urls, config=run_config)
        for result in results:
            if result.success:
                print(f"[OK] {result.url}, length: {len(result.markdown_v2.raw_markdown)}")
                await process_result(result, debug_mode=debug_mode)
            else:
                print(f"Failed to crawl {result.url}: {result.error_message}")

if __name__ == "__main__":
    import sys
    
    # Default values
    url = "https://ashoka.edu.in/home/"
    max_pages = 1
    debug = True
    
    # Command line argument handling
    if len(sys.argv) > 1:
        url = sys.argv[1]
    if len(sys.argv) > 2:
        max_pages = int(sys.argv[2])
    if len(sys.argv) > 3:
        debug = sys.argv[3].lower() == 'true'
    
    print(f"Starting crawler with URL: {url}, max_pages: {max_pages}, debug_mode: {debug}")
    asyncio.run(crawl_streaming(url, max_pages=max_pages, debug_mode=debug))