from enum import Enum

from pydantic import BaseModel, Field

from .utils import RoleFetcher


async def get_roles():
    fetcher = RoleFetcher()
    try:
        result = await fetcher.list_roles()
        return result.get("roles", [])
    except Exception as e:
        print(f"Error: {e}")


class Roles(Enum):
    Computer_Hardware_Engineer = "Computer Hardware Engineer"
    Linux_Admin = "Linux Admin"
    Manager = "Manager"
    cloud_engineer = "cloud engineer"


class Role(BaseModel):
    role_name: Roles = Field(..., description="Name of the role")
