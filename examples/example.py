from comparedocs import Comparator


def compare_my_text_files():
    # create new comparator and give
    # the comparator document you wish
    # to use for comparison

    doc_comp = Comparator('./text-files/Example.docx')

    # load files you wish to compare
    # your text file against
    doc_comp.add_document('./text-files/Example.pdf')
    doc_comp.add_document('./text-files/romeo-and-juliet.txt')

    results = doc_comp.compare()
    print(results)


if __name__ == "__main__":
    compare_my_text_files()