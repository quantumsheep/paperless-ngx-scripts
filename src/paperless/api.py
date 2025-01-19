from dataclasses import dataclass

import requests
from dict2dataclass import FromDict, ToDict


@dataclass(kw_only=True)
class Permission(FromDict, ToDict):
    users: list[int]
    groups: list[int]


@dataclass(kw_only=True)
class Permissions(FromDict, ToDict):
    view: Permission
    change: Permission


@dataclass(kw_only=True)
class Object:
    owner: int | None
    """
    Owner of the document.
    """

    permissions: Permissions
    """
    Allows setting document permissions. Optional, write-only
    """


@dataclass(kw_only=True)
class CustomField(FromDict, ToDict):
    field: int
    value: str


@dataclass(kw_only=True)
class Document(Object, FromDict, ToDict):
    id: int
    """
    ID of the document.
    """

    title: str
    """
    Title of the document.
    """

    content: str
    """
    Plain text content of the document.
    """

    tags: list[int]
    """
    List of IDs of tags assigned to this document, or empty list.
    """

    document_type: int | None
    """
    Document type of this document, or null.
    """

    correspondent: int | None
    """
    Correspondent of this document or null.
    """

    created: str
    """
    The date time at which this document was created.
    """

    created_date: str
    """
    The date (YYYY-MM-DD) at which this document was created. Optional. If also passed with created, this is ignored.
    """

    modified: str
    """
    The date at which this document was last edited in paperless.
    """

    added: str
    """
    The date at which this document was added to paperless.
    """

    archive_serial_number: str | None
    """
    The identifier of this document in a physical document archive.
    """

    original_file_name: str
    """
    Verbose filename of the original document.
    """

    archived_file_name: str | None
    """
    Verbose filename of the archived document. Null if no archived document is available.
    """

    notes: list[str]
    """
    Array of notes associated with the document.
    """

    page_count: int
    """
    Number of pages.
    """

    custom_fields: list[CustomField]
    """
    Array of custom fields & values.
    """


class Client:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        headers = {"Authorization": f"Token {self.token}"}
        return requests.request(method, url, headers=headers, **kwargs)

    def get_document(self, document_id: str) -> Document:
        response = self.request(
            "GET", f"{self.base_url}/api/documents/{document_id}/?full_perms=true"
        )
        response.raise_for_status()
        return Document.from_dict(response.json())

    def update_document(self, document: Document) -> Document:
        response = self.request(
            "PATCH",
            f"{self.base_url}/api/documents/{document.id}/",
            json=document.to_dict(),
        )
        response.raise_for_status()
        return Document.from_dict(response.json())
