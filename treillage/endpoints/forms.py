from typing import List, Union
from .. import ConnectionManager
from ..classes import DataObject, Identifier
from .list_paginator import list_paginator
from treillage import TreillageValidationException
import json

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                              Forms
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# GET Get Form
async def get_form(
    connection: ConnectionManager,
    project_id: Union[Identifier, int],
    section_selector: str,
    requested_fields: List[str] = [""],
):
    endpoint = f"/core/projects/{project_id}/forms/{section_selector}"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    return await connection.get(endpoint, params)


# POST Update Form
async def update_form(
    connection: ConnectionManager,
    project_id: Union[Identifier, int],
    section_selector: str,
    data_object: DataObject,
):
    body = data_object.body()
    if isinstance(project_id, Identifier):
        id = project_id.native
    else:
        id = project_id
    endpoint = f"/core/projects/{id}/forms/{section_selector}"
    if body == {}:
        raise TreillageValidationException("Body is empty.")
    return await connection.patch(endpoint, body)
