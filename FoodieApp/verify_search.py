import requests
import json

BASE_URL = "http://localhost:5000/api/v1"

def test_search():
    print("="*60)
    print("TESTING SEARCH FUNCTIONALITY")
    print("="*60)

    # Ensure some data exists
    # We rely on populate_sample_data.py having been run, or we can just try searching
    # Let's populate some data first just in case
    
    # 1. Search by Location (Mumbai)
    print("\n1. Testing Search by Location 'Mumbai'...")
    response = requests.get(f"{BASE_URL}/restaurants/search?location=Mumbai")
    if response.status_code == 200:
        results = response.json()['restaurants']
        print(f"✅ Found {len(results)} restaurants in Mumbai")
        for r in results:
            print(f"   - {r['name']} ({r['location']})")
    else:
        print(f"❌ Failed: {response.text}")

    # 2. Search by Name (Spice)
    print("\n2. Testing Search by Name 'Spice'...")
    response = requests.get(f"{BASE_URL}/restaurants/search?name=Spice")
    if response.status_code == 200:
        results = response.json()['restaurants']
        print(f"✅ Found {len(results)} restaurants matching 'Spice'")
        for r in results:
             print(f"   - {r['name']}")
    else:
        print(f"❌ Failed: {response.text}")

    # 3. Search by Category (Italian)
    print("\n3. Testing Search by Category 'Italian'...")
    response = requests.get(f"{BASE_URL}/restaurants/search?category=Italian")
    if response.status_code == 200:
        results = response.json()['restaurants']
        print(f"✅ Found {len(results)} Italian restaurants")
        for r in results:
             print(f"   - {r['name']} ({r['category']})")
    else:
        print(f"❌ Failed: {response.text}")

    # 4. Search by Non-existent Location (Bihar)
    print("\n4. Testing Search by Location 'Bihar' (Should be empty initially)...")
    response = requests.get(f"{BASE_URL}/restaurants/search?location=Bihar")
    if response.status_code == 200:
        results = response.json()['restaurants']
        print(f"✅ Query successful. Found {len(results)} results.")
    else:
        print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    test_search()
