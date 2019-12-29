import re
import string
import numpy as np
from math import log

from typing import List
from .document import Document


class CountVectorizer:

    @staticmethod
    def split_iter(document):
        return (x.group(0) for x in re.finditer(r"[A-Za-z0-9]+", document))

    def clean_document(self, document: str) -> str:
        """
        Cleans text from any punctuation characters and lowers it.
        Args:
            document: Text to be cleaned.

        Returns: Lowered string wihout punctuation sings.
        """
        return document.lower().translate(str.maketrans("", "", string.punctuation))

    def count_term_freq(self, document: Document) -> dict:
        document = self.clean_document(document.content)
        term_frequency = dict()
        for word in self.split_iter(document):
            if word in term_frequency:
                term_frequency[word] += 1
            else:
                term_frequency[word] = 1
        return term_frequency

    def vectorize(self, document):
        return np.array(list(self.count_term_freq(document).values()))


class TfidfVectorizer(CountVectorizer):

    def calculate_tfidf(self, term_freq: int, inverse_doc_freq: float) -> float:
        return term_freq * inverse_doc_freq

    def calculate_inverse_doc_freq(self, doc_num: int, term_doc_freq: int) -> float:
        return log(doc_num / term_doc_freq)

    def count_term_doc_freq(self, term: str, document: Document) -> int:
        return self.count_term_freq(document).get(term, 0)

    def vectorize(self, document: Document, comp_documents: List[Document]):
        term_frequencies = self.count_term_freq(document)
        doc_number = len(comp_documents)
        term_docs_frequencies = dict()
        for comp_doc in comp_documents:
            for term in term_frequencies.keys():
                if term not in term_docs_frequencies:
                    term_docs_frequencies[term] = 1
                term_docs_frequencies[term] += 1 if self.count_term_doc_freq(term, comp_doc) else 0

        tfidf = list()
        for term in term_frequencies:
            term_freq = term_frequencies.get(term, 0)
            term_doc_freq = term_docs_frequencies.get(term, 1)
            inverse_term_freq = self.calculate_inverse_doc_freq(doc_number, term_doc_freq)
            tfidf.append(self.calculate_tfidf(term_freq, inverse_term_freq))

        return np.array(tfidf)
