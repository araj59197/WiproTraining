import requests
import threading
import time

urls = [
    "https://www.google.com",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.wikipedia.org"
]

def download_content(url, filename):
    """Downloads content from a URL and saves it to a file."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Downloaded {url} to {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def run_sequential():
    print("\n--- Starting Sequential Download ---")
    start_time = time.time()
    for i, url in enumerate(urls):
        filename = f"data{i+1}.txt"
        download_content(url, filename)
    end_time = time.time()
    return end_time - start_time

def run_threading():
    print("\n--- Starting Threaded Download ---")
    start_time = time.time()
    threads = []
    
    for i, url in enumerate(urls):
        filename = f"data{i+1}_threaded.txt"
        t = threading.Thread(target=download_content, args=(url, filename))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
        
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    seq_time = run_sequential()
    print(f"Total time taken (Sequential): {seq_time:.4f} seconds")
    
    thread_time = run_threading()
    print(f"Total time taken (Threading): {thread_time:.4f} seconds")
    
    print(f"\nSpeedup: {seq_time / thread_time:.2f}x")
