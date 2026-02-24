from enum import Enum

from langfuse import observe
from pydantic import BaseModel, Field

from .utils import RoleFetcher


@observe
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
    system_admin = "system admin"


class Role(BaseModel):
    role_name: Roles = Field(..., description="Name of the role")
