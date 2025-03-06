import asyncio
from article_scraper_agent import ArticleScraperAgent
import time

async def main():
    # List of URLs to scrape
    urls = [
        'https://techcrunch.com',
        'https://www.theverge.com/tech',
        'https://www.wired.com',
        'https://www.cnet.com/news/',
        'https://www.engadget.com',
        'https://arstechnica.com',
        'https://www.zdnet.com',
        'https://www.gizmodo.com',
        'https://www.digitaltrends.com',
        'https://www.techradar.com/news'
    ]

    # Create and start ArticleScraperAgents for each URL
    agents = [ArticleScraperAgent(f"ScraperAgent{i+1}") for i in range(len(urls))]
    agent_tasks = [asyncio.create_task(agent.start()) for agent in agents]

    print(f"[{time.strftime('%H:%M:%S')}] Starting all agents...")

    # Send scrape messages to each agent and collect the scraping tasks
    scraping_tasks = []
    for agent, url in zip(agents, urls):
        print(f"[{time.strftime('%H:%M:%S')}] Sending scrape request to {agent.name} for {url}")
        scraping_tasks.append(agent.send({'type': 'scrape', 'url': url}))

    # Wait for all scraping tasks to complete
    print(f"[{time.strftime('%H:%M:%S')}] Waiting for agents to complete...")
    await asyncio.gather(*scraping_tasks)
    
    # Stop the agents
    for agent in agents:
        agent.stop()
    await asyncio.gather(*agent_tasks)

# Run the asyncio event loop
asyncio.run(main())
