import aiohttp


class RoleFetcher:
    """
    A class to asynchronously fetch roles from the API.
    """

    def __init__(self, base_url: str = "http://192.168.71.115"):
        """
        Initialize the RoleFetcher with the base URL of the API.

        Args:
            base_url (str): The base URL of the API (e.g., 'http://192.168.71.115').
        """
        self.base_url = base_url

    async def fetch_roles(self):
        """
        Asynchronously fetch roles from the API endpoint.

        Returns:
            dict: A dictionary containing the list of roles.

        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.base_url}/api/skills/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    roles = [item["role"] for item in data["data"]]
                    return {"roles": roles}
                else:
                    raise Exception(f"Failed to fetch data: HTTP {response.status}")

    async def list_roles(self):
        """
        Asynchronously list roles from the API.

        Returns:
            dict: A dictionary containing the list of roles.

        Raises:
            Exception: If the API request fails.
        """
        return await self.fetch_roles()
