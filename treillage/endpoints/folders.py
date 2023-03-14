from typing import List, Union
from .. import ConnectionManager
from ..classes import DataObject, Identifier
from .list_paginator import list_paginator
from treillage import TreillageValidationException
import json

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                              Folders
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# GET Get Folder Children
async def get_folder_children(
    connection: ConnectionManager,
    folder_id: int,
):
    endpoint = f"/core/folders/{folder_id}/children"

    return await connection.get(endpoint)


# POST Create Folder
async def create_folder(
    connection: ConnectionManager,
    parent_folder_id: int,
    project_id: int,
    folder_name: str,
):
    endpoint = f"/core/folders"
    body = {
        "parentId": {
            "native": parent_folder_id,
        },
        "projectId": {
            "native": project_id,
        },
        "name": folder_name,
    }
    return await connection.post(endpoint, body)
