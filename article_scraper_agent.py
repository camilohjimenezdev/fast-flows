import asyncio
from typing import Dict, Any
from actor import Actor
import aiohttp
from bs4 import BeautifulSoup
from openai import OpenAI
import base64
from PIL import Image
import time

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class ArticleScraperAgent(Actor):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.crop_height = 7000  # Make crop height configurable

    async def handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming messages to scrape and summarize articles."""
        if message['type'] == 'scrape':
            print(f"[{time.strftime('%H:%M:%S')}] {self.name} starting to scrape {message['url']}")
            url = message['url']
            response = await self.scrape_articles(url)
            print(f"[{time.strftime('%H:%M:%S')}] {self.name} finished scraping {message['url']}")
        else:
            response = "I don't understand."

        # print(f"Agent {self.name} response: {response}")

    async def scrape_articles(self, url: str) -> str:
        """Scrape articles from the given URL and return a summary."""
        import tempfile
        from playwright.async_api import async_playwright

        # Create a temporary file for the screenshot
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        screenshot_path = temp_file.name
        temp_file.close()

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            await page.screenshot(path=screenshot_path, full_page=True)
            await browser.close()

        # Crop the image to the configured height
        image = Image.open(screenshot_path)
        crop_height = min(self.crop_height, image.height)  # Ensure we don't crop beyond image height
        image = image.crop((0, 0, image.width, crop_height))
        image.save(screenshot_path)

        # Process the screenshot and get the summary
        result = await self.summarize_with_chatgpt(screenshot_path)
        print(screenshot_path)
        # Clean up the temporary file
        import os
        os.unlink(screenshot_path)
        
        return result

    async def summarize_with_chatgpt(self, image_path: str) -> str:
        try:
            client = OpenAI()

            # Getting the base64 string
            base64_image = encode_image(image_path)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Show me the main headlines from this image in a json format. The json should have the following fields: title, link, published_at. The published_at should be the date and time the article was published.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Error in summarization: {str(e)}"

