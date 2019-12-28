import string
import textract
from pathlib import Path


class Document:

    # TODO: Add Enum types for different document types
    __slots__ = {'name', 'path', 'type', '_dirty_content', '_content', 'embedded_content'}

    def __init__(self, path: str) -> None:
        path = Path(path)
        assert path.exists(), "Path provided for document is not valid."

        self.name = path.stem
        self.type = path.suffix
        self.content = textract.process(path).decode('utf-8')

    def embed_words(self):
        pass

    def clean_text(self, text: str) -> str:
        """
        Cleans text from any punctuation characters and lowers it.
        Args:
            text: Text to be cleaned.

        Returns: Lowered string wihout punctuation sings.
        """
        return text.lower().translate(str.maketrans('', '', string.punctuation))

    @property
    def content(self):
        """
        Returns original document content.
        """
        return self._dirty_content

    @content.setter
    def content(self, val: str):
        # cleans text before assigning it to _content
        self._content = self.clean_text(val)
        # assigns original text to `dirty_content` attribute
        self._dirty_content = val

