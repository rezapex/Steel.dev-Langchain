import asyncio
import requests
import json
from pprint import pprint

class SteelAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.steel.dev/v1"
        if not self.api_key:
            print("Warning: API key not provided. Please set the API_KEY environment variable or pass it to the constructor.")

    async def create_session(self, session_data=None):
        headers = {
            "Content-Type": "application/json",
            "steel-api-key": self.api_key
        }
        url = f"{self.base_url}/sessions"
        try:
            response = requests.post(url, headers=headers, data=json.dumps(session_data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating session: {e}")
            return None

    async def scrape(self, scrape_data):
        headers = {
            "Content-Type": "application/json",
            "steel-api-key": self.api_key
        }
        url = f"{self.base_url}/scrape"
        try:
            response = requests.post(url, headers=headers, data=json.dumps(scrape_data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during scrape: {e}")
            return None

    async def get_sessions(self):
        headers = {
            "steel-api-key": self.api_key
        }
        url = f"{self.base_url}/sessions"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting sessions: {e}")
            return None

    async def release_session(self, session_id):
        headers = {
            "Content-Type": "application/json",
            "steel-api-key": self.api_key
        }
        url = f"{self.base_url}/sessions/{session_id}/release"
        try:
            response = requests.post(url, headers=headers, data=json.dumps({}))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error releasing session: {e}")
            return None

    async def run(self):
        print("Steel agent running...")
        # Example usage:
        if self.api_key:
            session_data = {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "useProxy": True
            }
            session = await self.create_session(session_data)
            if session:
                print("\nSession created:")
                pprint(session)
                session_id = session.get("id")
                if session_id:
                    release_result = await self.release_session(session_id)
                    if release_result:
                        print("\nSession released:")
                        pprint(release_result)
            
            scrape_data = {
                "url": "https://www.example.com",
                "format": ["html", "markdown"]
            }
            scrape_result = await self.scrape(scrape_data)
            if scrape_result:
                print("\nScrape result:")
                pprint(scrape_result)
            
            sessions = await self.get_sessions()
            if sessions:
                print("\nSessions:")
                pprint(sessions)
        else:
            print("Please provide an API key to create a session.")
        await asyncio.sleep(1)
        print("Steel agent finished.")

if __name__ == "__main__":
    import os
    api_key = os.environ.get("STEEL_API_KEY")
    agent = SteelAgent(api_key=api_key)
    asyncio.run(agent.run())
