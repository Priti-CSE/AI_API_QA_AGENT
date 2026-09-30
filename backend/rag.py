import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


knowledge_folder = "knowledge"

documents = []


for filename in os.listdir(knowledge_folder):

    if filename.endswith(".txt"):

        file_path = os.path.join(knowledge_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:

            content = file.read()

        documents.append(
            Document(
                page_content=content,
                metadata={"source": filename}
            )
        )


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="chroma_db"
)


print("Knowledge documents loaded successfully.")
print("Documents:", len(documents))

query = "What status code means resource not found?"

results = vector_store.similarity_search(query, k=2)

print()
print("RAG SEARCH RESULTS")
print("==================")

for result in results:
    print(result.page_content)
    print("------------------")