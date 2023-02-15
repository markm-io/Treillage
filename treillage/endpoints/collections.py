from typing import List, Union
from .. import ConnectionManager
from ..classes import DataObject, Identifier
from .list_paginator import list_paginator
from treillage import TreillageValidationException
import json

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                              Collections
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# GET Get Form
async def get_collection_item(
    connection: ConnectionManager,
    project_id: Union[Identifier, int],
    section_selector: str,
    collection_item_id: Union[Identifier, int],
    requested_fields: List[str] = [""],
):
    endpoint = f"/core/projects/{project_id}/collections/{section_selector}/{collection_item_id}"
    params = dict()
    if isinstance(project_id, Identifier):
        proj_id = project_id.native
    else:
        proj_id = project_id
    if isinstance(project_id, Identifier):
        col_id = project_id.native
    else:
        col_id = project_id
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    endpoint = f"/core/projects/{proj_id}/collections/{section_selector}/{col_id}"

    return await connection.get(endpoint, params)


# POST Create Collection Item
async def create_collection_item(
    connection: ConnectionManager,
    project_id: Union[Identifier, int],
    section_selector: str,
    data_object: DataObject,
):
    if isinstance(project_id, Identifier):
        proj_id = project_id.native
    else:
        proj_id = project_id

    endpoint = f"/core/projects/{proj_id}/collections/{section_selector}/"
    data = data_object.body()
    if data == {}:
        raise TreillageValidationException("Body is empty.")
    body = dict(dataObject=data)
    return await connection.post(endpoint, body)


# PATCH Create Collection Item
async def update_collection_item(
    connection: ConnectionManager,
    project_id: Union[Identifier, int],
    section_selector: str,
    collection_item_id: Union[Identifier, int],
    data_object: DataObject,
):
    endpoint = f"/core/projects/{project_id}/collections/{section_selector}/{collection_item_id}"
    if isinstance(project_id, Identifier):
        proj_id = project_id.native
    else:
        proj_id = project_id
    if isinstance(project_id, Identifier):
        col_id = project_id.native
    else:
        col_id = project_id

    endpoint = f"/core/projects/{proj_id}/collections/{section_selector}/{col_id}"
    data = data_object.body()
    if data == {}:
        raise TreillageValidationException("Body is empty.")
    body = dict(dataObject=data)
    print(json.dumps(body, indent=4))
    # return await connection.patch(endpoint, body)


# GET Get Collection Items
async def get_collection_item_list(
    connection: ConnectionManager,
    project_id: Union[Identifier, int],
    section_selector: str,
    requested_fields: List[str] = [""],
):
    endpoint = f"/core/projects/{project_id}/collections/{section_selector}"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    async for item in list_paginator(connection, endpoint, params):
        yield item
