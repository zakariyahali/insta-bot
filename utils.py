import requests
import os
from dotenv import load_dotenv
from instabot import Bot
from datetime import datetime

load_dotenv()

def generate_image(quote):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": quote,
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
    image_url = response.json()["data"][0]["url"]
    return image_url

def download_image(image_url, save_path):
    response = requests.get(image_url)
    with open(save_path, "wb") as file:
        file.write(response.content)

def post_to_instagram(image_path, caption):
    bot = Bot()
    bot.login(username=os.getenv("INSTAGRAM_USERNAME"), password=os.getenv("INSTAGRAM_PASSWORD"))
    bot.upload_photo(image_path, caption=caption)

def save_and_post_image(quote, image_url):
    # Create the posts directory if it doesn't exist
    if not os.path.exists('posts'):
        os.makedirs('posts')
    
    # Save the image in the posts directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = f"posts/{timestamp}.jpg"
    download_image(image_url, image_path)

    # Post the image to Instagram
    post_to_instagram(image_path, quote)
