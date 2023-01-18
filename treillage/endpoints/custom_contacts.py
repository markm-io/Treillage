from typing import List
import json
from .. import ConnectionManager
from ..classes import Contact


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                             Custom Contacts
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# GET Custom Contact Metadata
async def get_contact_metadata(connection: ConnectionManager):
    endpoint = f"/core/custom-contacts-meta"
    return await connection.get(endpoint)


# POST Create Custom Contact
async def create_custom_contact(connection: ConnectionManager, body=Contact):
    endpoint = f"/core/custom-contacts"
    return await connection.post(endpoint, body.build_body_custom(), {})
