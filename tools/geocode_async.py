import asyncio
import httpx


async def reverse_geocode(lat, lon):
    async with httpx.AsyncClient() as client:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        response = await client.get(url)
        data = response.json()
        return data
    

async def main():
    locations = [( -23.5505, -46.6333), (40.7128, -74.0060), (48.8566, 2.3522)]
    
    tasks = [reverse_geocode(lat, lon) for lat, lon in locations]
    
    results = await asyncio.gather(*tasks)
    
    for location, result in zip(locations, results):
        address = result.get("display_name", "N/A")
        print(f"Location: {location} has address: {address}\n")


if __name__ == '__main__':
    asyncio.run(main())