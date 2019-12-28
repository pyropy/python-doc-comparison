from typing import Dict, List

from .document import Document


class Comparator:
    """
    API used for loading and comparing documents.
    """

    def __init__(self, path: str) -> None:
        self.doc = self.load_document(path)

    def load_document(self, path: str) -> Document:
        pass

    def compare(self, documents: List[Document]) -> Dict[str, float]:
        """
        Compares selected document again given documents,
        returns comparison results as dictionary of percentages.
        """
        pass
