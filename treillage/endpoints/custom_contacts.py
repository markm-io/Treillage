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
async def create_custom_contact(connection: ConnectionManager, contact: Contact):
    endpoint = f"/core/custom-contacts"
    body = contact.build_body_custom()
    return await connection.post(endpoint, body, {})


# PATCH Create Custom Contact
async def update_custom_contact(
    connection: ConnectionManager, contact: Contact, contact_id: int
):
    endpoint = f"/core/custom-contacts/{contact_id}"
    body = contact.build_body_custom()
    return await connection.patch(endpoint, body, {})
