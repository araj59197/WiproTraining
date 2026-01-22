import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse

class WebScraper:
    """A web scraper that fetches, parses, and extracts data from HTML pages."""
    
    def __init__(self, url):
        """Initialize the scraper with a target URL."""
        self.url = url
        self.soup = None
        self.data = {
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'title': None,
            'links': [],
            'tables': [],
            'lists': []
        }
    
    def fetch_page(self):
        """Fetch the HTML content from the URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None
    
    def parse_html(self, html_content):
        """Parse HTML content using BeautifulSoup with lxml parser."""
        if html_content:
            self.soup = BeautifulSoup(html_content, 'lxml')
            return True
        return False
    
    def extract_title(self):
        """Extract the page title."""
        if self.soup:
            title_tag = self.soup.find('title')
            self.data['title'] = title_tag.text.strip() if title_tag else "No title found"
            
            # Also try to get h1 as main heading
            h1_tag = self.soup.find('h1')
            self.data['main_heading'] = h1_tag.text.strip() if h1_tag else None
    
    def extract_links(self, max_links=50):
        """Extract all hyperlinks from the page."""
        if self.soup:
            links = []
            for link in self.soup.find_all('a', href=True)[:max_links]:
                href = link['href']
                # Convert relative URLs to absolute
                absolute_url = urljoin(self.url, href)
                
                link_data = {
                    'text': link.text.strip() or 'No text',
                    'href': absolute_url,
                    'is_external': self._is_external_link(absolute_url)
                }
                links.append(link_data)
            
            self.data['links'] = links
            self.data['link_count'] = len(links)
    
    def _is_external_link(self, link_url):
        """Check if a link is external to the current domain."""
        base_domain = urlparse(self.url).netloc
        link_domain = urlparse(link_url).netloc
        return base_domain != link_domain and link_domain != ''
    
    def extract_tables(self, max_tables=5):
        """Extract data from HTML tables."""
        if self.soup:
            tables = []
            for idx, table in enumerate(self.soup.find_all('table')[:max_tables]):
                table_data = {
                    'table_id': idx + 1,
                    'headers': [],
                    'rows': []
                }
                
                # Extract headers
                headers = table.find_all('th')
                if headers:
                    table_data['headers'] = [th.text.strip() for th in headers]
                
                # Extract rows
                for row in table.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        row_data = [cell.text.strip() for cell in cells]
                        table_data['rows'].append(row_data)
                
                if table_data['rows']:
                    tables.append(table_data)
            
            self.data['tables'] = tables
            self.data['table_count'] = len(tables)
    
    def extract_lists(self, max_lists=10):
        """Extract unordered and ordered lists."""
        if self.soup:
            lists = []
            
            # Extract unordered lists
            for idx, ul in enumerate(self.soup.find_all('ul')[:max_lists]):
                list_items = [li.text.strip() for li in ul.find_all('li', recursive=False)]
                if list_items:
                    lists.append({
                        'type': 'unordered',
                        'list_id': idx + 1,
                        'items': list_items
                    })
            
            # Extract ordered lists
            for idx, ol in enumerate(self.soup.find_all('ol')[:max_lists]):
                list_items = [li.text.strip() for li in ol.find_all('li', recursive=False)]
                if list_items:
                    lists.append({
                        'type': 'ordered',
                        'list_id': idx + 1,
                        'items': list_items
                    })
            
            self.data['lists'] = lists
            self.data['list_count'] = len(lists)
    
    def extract_metadata(self):
        """Extract meta tags and other metadata."""
        if self.soup:
            metadata = {}
            
            # Extract meta description
            meta_desc = self.soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                metadata['description'] = meta_desc['content']
            
            # Extract meta keywords
            meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords and meta_keywords.get('content'):
                metadata['keywords'] = meta_keywords['content']
            
            # Extract Open Graph data
            og_title = self.soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                metadata['og_title'] = og_title['content']
            
            self.data['metadata'] = metadata
    
    def scrape(self):
        """Execute the complete scraping process."""
        print(f"Fetching page: {self.url}")
        html_content = self.fetch_page()
        
        if not html_content:
            print("Failed to fetch page content")
            return None
        
        print("Parsing HTML...")
        if not self.parse_html(html_content):
            print("Failed to parse HTML")
            return None
        
        print("Extracting data...")
        self.extract_title()
        self.extract_links()
        self.extract_tables()
        self.extract_lists()
        self.extract_metadata()
        
        print("Scraping completed successfully!")
        return self.data
    
    def save_to_json(self, filename=None):
        """Save extracted data to a JSON file."""
        if filename is None:
            # Create filename from domain and timestamp
            domain = urlparse(self.url).netloc.replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"scraped_data_{domain}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return None
    
    def print_summary(self):
        """Print a summary of extracted data."""
        print("\n" + "="*60)
        print("SCRAPING SUMMARY")
        print("="*60)
        print(f"URL: {self.data['url']}")
        print(f"Title: {self.data['title']}")
        print(f"Links found: {self.data.get('link_count', 0)}")
        print(f"Tables found: {self.data.get('table_count', 0)}")
        print(f"Lists found: {self.data.get('list_count', 0)}")
        print("="*60 + "\n")


def main():
    """Main function to demonstrate the web scraper."""
    
    # Example URL - you can change this to any webpage
    # Using Wikipedia as an example (respects robots.txt)
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    
    # Alternative examples:
    # url = "https://www.python.org"
    # url = "https://example.com"
    
    # Create scraper instance
    scraper = WebScraper(url)
    
    # Perform scraping
    data = scraper.scrape()
    
    if data:
        # Print summary
        scraper.print_summary()
        
        # Display sample of extracted data
        print("\nSample Links (first 5):")
        for i, link in enumerate(data['links'][:5], 1):
            print(f"{i}. {link['text'][:50]} -> {link['href'][:60]}")
        
        if data['tables']:
            print(f"\nFound {len(data['tables'])} table(s)")
            print(f"First table has {len(data['tables'][0]['rows'])} rows")
        
        if data['lists']:
            print(f"\nFound {len(data['lists'])} list(s)")
            print(f"First list has {len(data['lists'][0]['items'])} items")
        
        # Save to JSON file
        scraper.save_to_json()
        
        # Optionally save with custom filename
        # scraper.save_to_json('my_scraped_data.json')
    else:
        print("Scraping failed!")


if __name__ == "__main__":
    main()