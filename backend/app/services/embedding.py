from sentence_transformers import SentenceTransformer
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            # Load model (lazy loading)
            # using 'all-MiniLM-L6-v2' for balance of speed and quality
            cls._model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._model

    @classmethod
    def generate(cls, text: str) -> list[float]:
        model = cls.get_model()
        # encode returns numpy array, convert to list
        embedding = model.encode(text)
        return embedding.tolist()

    @classmethod
    def generate_batch(cls, texts: list[str]) -> list[list[float]]:
        model = cls.get_model()
        embeddings = model.encode(texts)
        return embeddings.tolist()
