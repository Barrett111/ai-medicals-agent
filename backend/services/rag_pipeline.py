from backend.services.retriever import get_retriever
from backend.services.llm import generate_response
from backend.services.web_search import web_search
import json
import re
import logging

logging.basicConfig(level=logging.INFO)


# ✅ Safe JSON parser
def safe_json(text):
    if not text:
        return {
            "answer": "LLM failed to generate response",
            "confidence": 0,
            "source": "llm-error"
        }

    try:
        return json.loads(text)
    except:
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass

        return {
            "answer": text.strip(),
            "confidence": 0.6,
            "source": "llm-fallback"
        }


# ✅ Core pipeline
def get_answer(query: str):
    try:
        logging.info(f"Query: {query}")

        # 🔥 FIX: Load retriever ONLY when needed
        retriever = get_retriever()

        if retriever is None:
            logging.warning("Retriever not available, using web fallback")
        else:
            # 🔹 Step 1: Retrieve documents
            docs = retriever.invoke(query)

            if docs:
                context = "\n\n".join([doc.page_content for doc in docs[:6]])

                # 🔹 Step 2: Relevance check
                relevance_prompt = f"""
Answer ONLY YES or NO.

Context:
{context}

Question: {query}

Is this context useful?
"""
                relevance = generate_response(relevance_prompt) or ""
                logging.info(f"Relevance: {relevance}")

                if relevance.strip().upper().startswith("YES"):

                    # 🔥 Main answer prompt
                    prompt = f"""
You are a medical assistant.

Give a DETAILED and structured answer.

Rules:
- Use headings
- Use bullet points
- Explain clearly like a doctor
- Include causes, symptoms, stages, treatment if applicable

Context:
{context}

Question: {query}

Return ONLY JSON:
{{
  "answer": "detailed structured answer",
  "confidence": 0.9,
  "source": "document"
}}
"""

                    llm_output = generate_response(prompt)
                    logging.info(f"LLM (doc): {llm_output}")

                    return safe_json(llm_output)

        # 🔥 Step 3: Web fallback
        logging.info("Using web fallback")

        web_data = web_search(query)

        fallback_prompt = f"""
You are a medical AI assistant.

Use the web data and your knowledge.

Give a DETAILED structured answer:
- Headings
- Bullet points
- Explanation
- Medical clarity

Web Data:
{web_data}

Question: {query}

Return ONLY JSON:
{{
  "answer": "detailed structured answer",
  "confidence": 0.8,
  "source": "web+llm"
}}
"""

        llm_output = generate_response(fallback_prompt)
        logging.info(f"LLM (web): {llm_output}")

        return safe_json(llm_output)

    except Exception as e:
        logging.error(f"Pipeline Error: {str(e)}")

        return {
            "answer": f"Pipeline error: {str(e)}",
            "confidence": 0,
            "source": "system-error"
        }