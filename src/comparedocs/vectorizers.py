import re
import string
import numpy as np
from math import log

from typing import List
from collections import Counter
from .document import Document


class CountVectorizer:

    @staticmethod
    def split_iter(document_content: str):
        """
        Splits document in words and returns it as generator.
        Args:
            document_content: Cleaned document content.

        Returns: Generator of document terms.
        """
        return (x.group(0) for x in re.finditer(r"[A-Za-z0-9]+", document_content))

    def clean_document(self, document: str) -> str:
        """
        Cleans text from any punctuation characters and lowers it.
        Args:
            document: Text to be cleaned.

        Returns: Lowered string wihout punctuation sings.
        """
        return document.lower().translate(str.maketrans("", "", string.punctuation))

    def count_term_freq(self, document: Document) -> dict:
        """
        Counts term frequency inside document.
        Args:
            document: Loaded document object.

        Returns: Counter with term: count items.
        """
        document = self.clean_document(document.content)
        return Counter(document)

    def vectorize(self, document: Document) -> np.ndarray:
        """
        Counts document term frequency and returns it as vecotr.
        Args:
            document: Loaded document object.

        Returns: Numpy array with term frequency values.
        """
        return np.array(list(self.count_term_freq(document).values()))


class TfidfVectorizer(CountVectorizer):

    def calculate_tfidf(self, term_freq: int, inverse_doc_freq: float) -> float:
        """
        Calculates term frequency - inverse document frequency.
        Args:
            term_freq: Term frequency.
            inverse_doc_freq: Inverse document frequency.

        Returns: Product of term and inverse document frequency (float).
        """
        return term_freq * inverse_doc_freq

    def calculate_inverse_doc_freq(self, doc_num: int, term_doc_freq: int) -> float:
        """
        Calculates inverse document frequency.
        Args:
            doc_num: Number of documents.
            term_doc_freq: Number of term apperances in documents.

        Returns: Inverse document frequency (float).
        """
        return log(doc_num / term_doc_freq)

    def count_term_doc_freq(self, term: str, document: Document) -> int:
        """
        Returns number of appearances of term for given document.
        Args:
            term: String.
            document: Loaded document object.

        Returns: Number of appearances of term for given document.
        """
        return self.count_term_freq(document).get(term, 0)

    def vectorize(self, document: Document, comp_documents: List[Document]) -> np.ndarray:
        """
        Calculates TFIDF for given documents and returns it as matrix (numpy array).
        Args:
            document: Loaded document.
            comp_documents: List of loaded documents.

        Returns: Matrix (numpy array) representing TFIDF.
        """
        term_frequencies = self.count_term_freq(document)
        doc_number = len(comp_documents)
        term_docs_frequencies = dict()
        for comp_doc in comp_documents:
            for term in term_frequencies.keys():
                if term not in term_docs_frequencies:
                    term_docs_frequencies[term] = 1
                term_docs_frequencies[term] += 1 if self.count_term_doc_freq(term, comp_doc) else 0

        _tfidf = list()
        for term in term_frequencies:
            term_freq = term_frequencies.get(term, 0)
            term_doc_freq = term_docs_frequencies.get(term, 1)
            inverse_term_freq = self.calculate_inverse_doc_freq(doc_number, term_doc_freq)
            _tfidf.append(self.calculate_tfidf(term_freq, inverse_term_freq))

        return np.array(_tfidf)
