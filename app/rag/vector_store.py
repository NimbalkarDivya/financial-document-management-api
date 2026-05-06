import chromadb

client = chromadb.Client()

collection = client.create_collection("financial_documents")


def add_chunks(chunks):

    for index, chunk in enumerate(chunks):

        collection.add(
            documents=[chunk],
            ids=[str(index)]
        )


def search_chunks(query):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    return results