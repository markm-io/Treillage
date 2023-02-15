from typing import List, Union
from .. import ConnectionManager
from ..classes import Project
from .list_paginator import list_paginator
import json

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                              Projects
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# GET Project
async def get_project(
    connection: ConnectionManager,
    project_id: int,
    requested_fields: List[str] = [""],
):
    endpoint = f"/core/project/{project_id}"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    return await connection.get(endpoint, params)


# GET Project List
async def get_project_list(
    connection: ConnectionManager,
    requested_fields: List[str] = [""],
):
    endpoint = "/core/projects"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    async for project in list_paginator(connection, endpoint, params):
        yield project


# GET Project Vitals
async def get_project_vitals(
    connection: ConnectionManager,
    project_id: int,
    requested_fields: List[str] = [""],
):
    endpoint = f"/core/project/{project_id}"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    return await connection.get(endpoint, params)


# POST Create Project
async def create_project(
    connection: ConnectionManager,
    project: Project,
):
    project = vars(project)
    endpoint = f"/core/projects"
    return await connection.post(endpoint, project)


## MOVE THIS SOMEWHERE ELSE!!
# POST Toggle Section Visibility
async def update_section_visibility(
    connection: ConnectionManager,
    project_id: int,
    body: dict,
):
    endpoint = f"/core/projects/{project_id}/sectionvisibility"
    return await connection.post(endpoint, body)
