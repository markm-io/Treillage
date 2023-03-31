from typing import List
from .. import ConnectionManager
from .. import TreillageTypeError, TreillageValueError
from .list_paginator import list_paginator


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                              Project Types
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# GET Project Type
async def get_project_type(
    connection: ConnectionManager,
    project_type_id: int,
    requested_fields: List[str] = [""],
):
    endpoint = f"/core/projecttypes/{project_type_id}"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    return await connection.get(endpoint, params)


async def get_project_type_list(
    connection: ConnectionManager, requested_fields: List[str] = [""], **kwargs
):
    endpoint = "/core/projecttypes"
    params = dict()
    for key, value in kwargs.items():
        params[str(key)] = value
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    async for contact in list_paginator(connection, endpoint, params):
        yield contact


async def get_project_type_section(
    connection: ConnectionManager,
    project_type_id: int,
    section_selector: str,
    requested_fields: List[str] = [""],
):
    endpoint = f"/core/projecttypes/{project_type_id}/sections/{section_selector}"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    return await connection.get(endpoint, params)


# GET Project Type Section List
async def get_project_type_section_list(
    connection: ConnectionManager,
    project_type_id: int,
    requested_fields: List[str] = [""],
):
    endpoint = f"/core/projecttypes/{project_type_id}/sections"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    return await connection.get(endpoint, params)


# GET Project Type Phase List
async def get_project_type_phase_list(
    connection: ConnectionManager,
    project_type_id: int,
    requested_fields: List[str] = [""],
):
    endpoint = f"core/projecttypes/{project_type_id}/phases"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    return await connection.get(endpoint, params)


# GET Org Info
async def get_org_info(
    connection: ConnectionManager,
    requested_fields: List[str] = [""],
):
    endpoint = "/core/users/me"
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields

    return await connection.get(endpoint, params)
