import chromadb

client = chromadb.PersistentClient("./my_db")
coll = client.get_or_create_collection(name="study")

coll.upsert(
    documents=["파이썬 완벽 가이드"],
    metadatas=[{"lang":"python", "year":2024, "official":True}],
    ids=["id1"]
)

coll.upsert(
    documents=["자바 성능 최적화"],
    metadatas=[{"lang":"java", "year":2022, "official":False}],
    ids=["id2"]
)

coll.upsert(
    documents=["리액트 기초 실습"],
    metadatas=[{"lang":"javascript", "year":2023, "official":True}],
    ids=["id3"]
)

print(coll.get())
