from .identifier import Identifier
from typing import Union


class Note:
    def __init__(
        self,
        body: str,
        project_id: Union[Identifier, int],
        author_id: Union[Identifier, int],
        note_id: Union[Identifier, int, None] = None,
    ):
        self.body = body
        if type(project_id) == Identifier:
            self.projectId = project_id
        elif type(project_id) == int:
            self.projectId = Identifier(native=project_id)
        if type(author_id) == Identifier:
            self.authorId = author_id
        elif type(author_id) == int:
            self.authorId = Identifier(native=author_id)
        if type(note_id) == Identifier:
            self.noteId = note_id
        elif type(note_id) == int:
            self.noteId = Identifier(native=note_id)
