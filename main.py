from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from utils import generate_image, save_and_post_image
from schemas import Quote

app = FastAPI()

load_dotenv()

@app.get("/get-quote", response_model=Quote)
def get_quote():
    url = "https://love-quote.p.rapidapi.com/lovequote"
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "love-quote.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    quote = response.json().get("quote")
    print(f"Retrieved quote: {quote}")
    return {"quote": quote}

@app.post("/generate-and-post")
def generate_and_post():
    quote_data = get_quote()
    quote = quote_data["quote"]
    image_url = generate_image(quote)
    save_and_post_image(quote, image_url)
    return {"message": "Post created successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
