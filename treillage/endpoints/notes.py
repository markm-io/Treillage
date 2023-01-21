from typing import List, Union
from .. import ConnectionManager
from ..classes import Note, Identifier
from .list_paginator import list_paginator

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                              Notes
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# GET Get Note
async def get_note(
    connection: ConnectionManager,
    note_id: Union[Identifier, int],
    requested_fields: List[str] = [""],
):
    params = dict()
    if not requested_fields == [""]:
        fields = ",".join(*[requested_fields])
        params["requestedFields"] = fields
    if isinstance(note_id, Identifier):
        note_id = note_id.native
    endpoint = f"/core/notes/{note_id}/"
    return await connection.get(endpoint, params)


# POST Create Note
async def create_note(connection: ConnectionManager, note: Note):

    endpoint = f"/core/notes/"
    body = vars(note)
    return await connection.post(endpoint, body)
