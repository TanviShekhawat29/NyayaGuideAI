from groq import Groq
import os

# 🔐 Read API key from environment (Cloud Run safe)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL_NAME = "llama-3.3-70b-versatile"


def generate_llm_response(context, query):
    try:
        prompt = f"""
You are a legal assistant.

Context:
{context}

Question:
{query}

Explain clearly in simple legal language. Give a complete and helpful answer.
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM ERROR: {str(e)}"