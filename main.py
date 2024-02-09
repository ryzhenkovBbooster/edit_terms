# This is a sample Python script.
from edit_docs import read_doc
from search_docs import extract_document_id_from_url

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


urls = ''

if __name__ == '__main__':
    for url in urls:
        id = extract_document_id_from_url(url)
        read_doc(id)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
