import random
import requests
import os

SUBREDDITS = ["memes", "dankmemes", "wholesomememes"]

def get_reddit_meme():
    headers = {'User-Agent': 'Mozilla/5.0'}
    for subreddit in SUBREDDITS:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=30&t=day"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue
        posts = response.json().get("data", {}).get("children", [])
        for post in posts:
            data = post["data"]
            if data.get("post_hint") == "image" and not data.get("over_18"):
                # Return first suitable meme found
                return {
                    "url": data["url"],
                    "caption": data.get("title", "Funny Gen Z Meme from Reddit")
                }
    return None

def download_image(image_url):
    img_data = requests.get(image_url).content
    filename = "image.jpg"
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    return filename

def post_to_facebook(image_path, caption):
    page_token = os.getenv("FACEBOOK_MEME_PAGE_TOKEN")
    page_id = os.getenv("FACEBOOK_MEME_PAGE_ID")

    hashtags = "#GenZ #Meme #Funny #DailyMeme #RedditMeme #Laughter #Humor"
    full_caption = f"{caption}\n\n{hashtags}"

    files = {'source': open(image_path, 'rb')}
    payload = {'access_token': page_token, 'message': full_caption}
    post_url = f"https://graph.facebook.com/{page_id}/photos"

    response = requests.post(post_url, files=files, data=payload)
    print("Posted meme to Facebook:", response.json())

def main():
    try:
        meme = get_reddit_meme()
        if meme and meme.get("url"):
            image_path = download_image(meme["url"])
            post_to_facebook(image_path, meme["caption"])
    except Exception as e:
        print("Error posting meme:", e)

if __name__ == "__main__":
    main()
