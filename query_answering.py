from langchain.chat_models import ChatOllama
from db import PineconeVectorDB
import json

pinecone_db = PineconeVectorDB()

def get_answer(query: str):
    llm = ChatOllama(model="llama3.1", temperature=0)
    context = get_context(query, llm)

    full_prompt = f"""
    You are an AI designed to answer questions based on a given context. 
    Use only the information provided in the context to generate accurate 
    and concise responses.

    QUERY: {query}
    CONTEXT: {context['answer']}
    """

    result = llm.invoke(full_prompt)
    return result.content.strip()

def get_context(query, llm, iterations=2):
    try:
        answers = pinecone_db.query(query, top_k=5)
        answer = ""
        references = []

        for ans in answers["matches"]:
            answer += ans["metadata"]["content"]
            if ans["metadata"].get("path"):
                references.append(ans["metadata"]["path"])

        if iterations == 0:
            return {
                "is_sufficient": False,
                "answer": answer
            }

        prompt = f"""
        Query: '{query}'
        Context: '{answer}'
        Is the context sufficient? Return JSON format:
        {{
            "is_sufficient": true/false,
            "additional_info_needed": "details if insufficient",
            "modified_query": "updated query if needed"
        }}
        """

        result = llm.invoke(prompt)
        response = json.loads(result.content.strip())

        if response.get("is_sufficient", False):
            response['answer'] = answer
            return response

        return get_context(response.get("modified_query", query),
                           llm, iterations - 1)

    except Exception as e:
        return {"error": str(e)}
