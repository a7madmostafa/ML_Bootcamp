import requests
import os
from dotenv import load_dotenv

def welcome_message():
    print("Welcome to the News API Client!")
    

def get_top_headlines(api_key, keyword="technology", country="us"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "q": keyword,
        "country": country,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            print("No articles found.")
            return

        for i, article in enumerate(articles[:10], start=1):  # Show top 10
            print(f"\n📰 Headline {i}")
            print("Title:", article["title"])
            print("Source:", article["source"]["name"])
            print("URL:", article["url"])
    else:
        print("Error:", response.status_code)

def main():
    load_dotenv()  
    api_key = os.getenv("API_KEY")
    keyword = input("Enter your News keyword: ")
    country = input("Enter the country code (e.g., 'us' for United States): ")
    get_top_headlines(api_key, keyword, country)


if __name__ == "__main__":   # Run this script directly
    main()

