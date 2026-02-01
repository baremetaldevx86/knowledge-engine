from typing import List

class TextProcessor:
    @staticmethod
    def clean(text: str) -> str:
        # Basic cleaning: remove excessive whitespace
        return " ".join(text.split())

    @staticmethod
    def chunk(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        # Simple sliding window chunking
        # In production, use langchain's RecursiveCharacterTextSplitter or similar
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            current_chunk.append(word)
            current_length += len(word) + 1 # +1 for space
            
            if current_length >= chunk_size:
                chunks.append(" ".join(current_chunk))
                # Keep overlap for context
                overlap_words = []
                overlap_length = 0
                for w in reversed(current_chunk):
                    overlap_words.insert(0, w)
                    overlap_length += len(w) + 1
                    if overlap_length >= overlap:
                        break
                current_chunk = overlap_words
                current_length = overlap_length
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks
