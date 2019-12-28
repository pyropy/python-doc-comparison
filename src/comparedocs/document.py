import string
import textract
from pathlib import Path

import numpy as np


class Document:

    # TODO: Add Enum types for different document types
    __slots__ = {"name", "path", "type", "_dirty_content", "_content", "_vector"}

    def __init__(self, path: str = "") -> None:
        file = Path(path)
        assert file.exists(), "Path provided for document is not valid."

        self.name = file.stem
        self.type = file.suffix
        self.content = textract.process(file).decode("utf-8")
        self._vector = None

    def to_vector(self):
        """
        Counts word frequency and transforms document to numpy array (vector)
        """
        word_frequency = dict()
        for word in self.content.split():
            if word not in word_frequency:
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1

        self._vector = np.array(list(word_frequency.values()))
        return self._vector

    def clean_text(self, text: str) -> str:
        """
        Cleans text from any punctuation characters and lowers it.
        Args:
            text: Text to be cleaned.

        Returns: Lowered string wihout punctuation sings.
        """
        return text.lower().translate(str.maketrans("", "", string.punctuation))

    @property
    def content(self):
        """
        Returns original document content.
        """
        return self._dirty_content

    @property
    def vector(self):
        if self._vector:
            return self._vector
        return self.to_vector()

    @content.setter
    def content(self, val: str):
        # cleans text before assigning it to _content
        self._content = self.clean_text(val)
        # assigns original text to `dirty_content` attribute
        self._dirty_content = val

