import textract
from pathlib import Path


class Document:

    # TODO: Add Enum types for different document types
    __slots__ = {'name', 'path', 'type', 'content'}

    def __init__(self, path: str) -> None:
        path = Path(path)
        assert path.exists(), "Path provided for document is not valid."

        self.name = path.stem
        self.type = path.suffix
        self.content = textract.process(path).decode('utf-8')

