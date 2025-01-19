import os
from abc import ABC, abstractmethod

from paperless.api import Client
from paperless.logger import Logger


def getenv(name: str, default: str | None = None) -> str:
    value = os.environ.get(name) or default
    if value is None:
        raise ValueError(f"{name} environment variable is required")
    return value


class PostConsumptionScriptEnvironmentVariables:
    def __init__(self):
        self.document_id = getenv("DOCUMENT_ID")
        self.document_file_name = getenv("DOCUMENT_FILE_NAME")
        self.document_archive_path = getenv("DOCUMENT_ARCHIVE_PATH", "")
        self.document_source_path = getenv("DOCUMENT_SOURCE_PATH")
        self.document_created = getenv("DOCUMENT_CREATED")
        self.document_added = getenv("DOCUMENT_ADDED")
        self.document_modified = getenv("DOCUMENT_MODIFIED")
        self.document_thumbnail_path = getenv("DOCUMENT_THUMBNAIL_PATH")
        self.document_download_url = getenv("DOCUMENT_DOWNLOAD_URL")
        self.document_thumbnail_url = getenv("DOCUMENT_THUMBNAIL_URL")
        self.document_owner = getenv("DOCUMENT_OWNER", "")
        self.document_correspondent = getenv("DOCUMENT_CORRESPONDENT", "")
        self.document_tags = list(filter(None, getenv("DOCUMENT_TAGS", "").split(",")))
        self.task_id = getenv("TASK_ID", "")


class PostConsumptionScript(ABC):
    def __init__(self, name: str):
        self.name = name
        self.env = PostConsumptionScriptEnvironmentVariables()

        base_url = getenv("PAPERLESS_SCRIPTS_BASE_URL", default="http://localhost:8000")
        token = getenv("PAPERLESS_SCRIPTS_TOKEN")

        self.client = Client(base_url, token)
        self.logger = Logger(name)

    def getenv(self, name: str, default: str | None = None) -> str:
        return getenv(
            f"PAPERLESS_POST_CONSUME_SCRIPT_{self.name.upper()}_{name.upper()}",
            default,
        )

    @abstractmethod
    def run(self): ...
