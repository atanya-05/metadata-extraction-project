from src.embeddings import EmbeddingModel

model = EmbeddingModel()

vector = model.encode(["Hello Agreement"])

print(vector.shape)