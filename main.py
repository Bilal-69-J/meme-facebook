import os
import requests

def post_to_facebook(image_path, caption):
    page_token = os.getenv("FACEBOOK_MEME_PAGE_TOKEN")
    page_id = os.getenv("FACEBOOK_MEME_PAGE_ID")

    # Debug environment variables (do NOT print token, just show if set)
    print("DEBUG: FACEBOOK_MEME_PAGE_ID =", page_id)
    print("DEBUG: FACEBOOK_MEME_PAGE_TOKEN set =", bool(page_token))

    if not page_token or not page_id:
        raise Exception("Facebook token or page ID is missing!")

    hashtags = "#GenZ #Meme #Funny #DailyMeme #RedditMeme #Laughter #Humor"
    full_caption = f"{caption}\n\n{hashtags}"

    try:
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            payload = {'access_token': page_token, 'message': full_caption}
            # Use explicit Graph API version for reliability
            post_url = f"https://graph.facebook.com/v17.0/{page_id}/photos"

            response = requests.post(post_url, files=files, data=payload)

            print("DEBUG: Facebook API Status Code:", response.status_code)
            print("DEBUG: Facebook API Response Text:", response.text)

            if response.status_code != 200:
                raise Exception(f"Facebook API Error: {response.text}")

            print("Post successful!")

    except Exception as e:
        print("Exception in post_to_facebook:", str(e))
        raise


if __name__ == "__main__":
    # Just to test environment variables are loaded properly before posting
    print("Testing environment variables...")
    print("FACEBOOK_MEME_PAGE_ID:", os.getenv("FACEBOOK_MEME_PAGE_ID"))
    print("FACEBOOK_MEME_PAGE_TOKEN set:", bool(os.getenv("FACEBOOK_MEME_PAGE_TOKEN")))

    # Example usage (replace with actual call in your main flow)
    # post_to_facebook("image.jpg", "Test meme caption")
