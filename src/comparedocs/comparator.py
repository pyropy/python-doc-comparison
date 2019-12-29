import numpy as np
from typing import Dict, List

from src.comparedocs.document import Document
from src.comparedocs.vectorizer import TfidfVectorizer, CountVectorizer


class Comparator:
    """
    API used for loading and comparing documents.
    """

    def __init__(self, path: str) -> None:
        self.doc = self.load_document(path)
        self.doc_vector = CountVectorizer().vectorize(self.doc)
        self.comp_docs = list()
        self.vectorizer = TfidfVectorizer()

    def add_document(self, path: str) -> None:
        self.comp_docs.append(self.load_document(path))

    def load_document(self, path: str) -> Document:
        """
        Loads and returns Document from given path.
        Args:
            path: Path to document.

        Returns: Document instance.
        """
        return Document(path)

    def calculate_vector_magnitude(self, vector: np.ndarray) -> float:
        """
        Calculates vector angle.
        Args:
            vector: Numpy array.
        """
        return np.sqrt(vector.dot(vector))

    def calculate_vector_angle(self, vector_1: np.ndarray, vector_2: np.ndarray) -> float:
        mag_vec_1 = self.calculate_vector_magnitude(vector_1)
        mag_vec_2 = self.calculate_vector_magnitude(vector_2)
        return vector_1.dot(vector_2) / mag_vec_1 / mag_vec_2

    def compare(self, documents: List[Document] = None) -> Dict[str, float]:
        if documents is None:
            documents = list()

        documents.extend(self.comp_docs)
        assert len(documents), "Please provide documents that " \
                               "you would like to compare your document to."

        result = dict()
        for comp_doc in iter(documents):
            result[comp_doc.name] = self._compare(comp_doc)
        return result

    def _compare(self, document: Document) -> float:
        """
        Compares selected document again given documents,
        returns comparison results as dictionary of document names
        and their percentage similarities.
        """
        tfidf = self.vectorizer.vectorize(self.doc, [document])
        return self.calculate_vector_angle(self.doc_vector, tfidf)

