from sentence_transformers import SentenceTransformer
import time

print("Loading model...")
start = time.time()
model = SentenceTransformer('all-MiniLM-L6-v2')
end = time.time()
print(f"Model loaded in {end - start:.2f} seconds.")
print("Test encoding...")
vec = model.encode("Hello world")
print(f"Vector dimension: {len(vec)}")
print("Preload complete.")
