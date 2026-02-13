import requests
import threading
import time

urls = [
    "https://www.google.com",
    "https://www.yahoo.com",
    "https://www.rediff.com",
    "https://www.amazon.in",
]


def downloadfiles(url):
    try:
        response = requests.get(url)
        filename = url.split("/")[-1] + ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Downloaded:{filename}")
    except Exception as e:
        print(f"Error downloading{url}:{e}")


starttime = time.time()
for url in urls:
    downloadfiles(url)
sequentialtime = time.time() - starttime
print(f"\nsequential download time:{sequentialtime}")

threads = []
starttime1 = time.time()
for url in urls:
    t = threading.Thread(target=downloadfiles, args=(url,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

threadingtime = time.time() - starttime1
print(f"\nthreading download time:{threadingtime}")
