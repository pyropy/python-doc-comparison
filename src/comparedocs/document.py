import textract
from pathlib import Path

class Document:

    # TODO: Add Enum types for different document types
    __slots__ = {"name", "path", "type", "content"}

    def __init__(self, path: str = "") -> None:
        file = Path(path)
        assert file.exists(), "Path provided for document is not valid."

        self.name = file.name
        self.type = file.suffix
        self.content = textract.process(file).decode("utf-8")
