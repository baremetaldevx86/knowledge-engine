import os
from openai import AsyncOpenAI

class LLMService:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            
            base_url = os.getenv("OPENAI_BASE_URL")
            if not base_url and (api_key.startswith("sk-or-") or "openrouter" in api_key):
                 base_url = "https://openrouter.ai/api/v1"
            
            cls._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        return cls._client

    @classmethod
    async def generate_answer(cls, query: str, context: str) -> str:
        client = cls.get_client()
        
        system_prompt = """You are a helpful personal knowledge assistant.
        
        You have access to the user's notes.
        The user may ask questions about a specific document or general questions.
        
        CRITICAL INSTRUCTION:
        If the context contains a source labeled [MOST_RECENT_UPLOAD START] or [MOST_RECENT_UPLOAD], you must prioritize this source for generic queries like "Summarize", "What is this document?", or "Table of Contents".
        Only use other [SEARCH_RESULT] sources if they are directly relevant to a specific keyword in the user's question.
        
        Answer the user's question based ONLY on the provided context.
        If the answer is not in the context, say "I couldn't find relevant information in your notes."
        """
        
        user_prompt = f"""
        Context:
        {context}
        
        Question:
        {query}
        
        Answer:
        """
        
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo", # OpenRouter maps this to a default free/cheap model usually
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3, 
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM API Failed: {e}. Using mock response.")
            # Fallback: simple extraction or canned response
            return f"**[Mock AI Response]** (OpenAI API Unavailable)\n\nBased on your notes, here is what I found:\n\n{context[:300]}...\n\n(This is a simulated answer because the API key was invalid or quota exceeded.)"
