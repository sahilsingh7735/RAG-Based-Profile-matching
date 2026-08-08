import chromadb


client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "resume_collection"
)

print("=" * 60)
print("CHROMADB CHECK")
print("=" * 60)

print("Total records:", collection.count())

results = collection.get(
    limit=10,
    include=["documents", "metadatas"]
)

for i, metadata in enumerate(
    results["metadatas"],
    start=1
):

    print("\nRecord:", i)

    print(
        "Name:",
        metadata.get("name")
    )

    print(
        "Skills:",
        metadata.get("skills")
    )

    print(
        "Experience:",
        metadata.get("experience_years")
    )

    print(
        "Education:",
        metadata.get("education")
    )

    print(
        "Section:",
        metadata.get("section")
    )

print("\n" + "=" * 60)