from tests.test_document import test_docs


for doc in test_docs.values():
    doc.write_to_file(f'tests/test_doc_contents/{doc.name}')