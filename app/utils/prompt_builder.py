from app.models.clinic import Clinic

def build_prompt(clinic: Clinic, rag_context: str) -> str:
    """
    Dynamically builds the system prompt for the AI based on clinic settings and RAG context.
    """
    
    # Base instructions
    prompt = f"""
You are a helpful, cheerful, and efficient AI assistant for {clinic.name}.
Your personality and tone should be: {clinic.ai_tone}.
You MUST respond in this language: {clinic.ai_language}.

Your primary tasks are to answer questions about the clinic, its services, and to help customers with inquiries like booking appointments.
Be concise, helpful, and stick to your role. Do not go off-topic or engage in casual conversation beyond what is necessary.
"""

    # Add services information if available
    if clinic.services:
        service_list = "\n".join([f"- {s.name}: {s.description or 'No description available'}. Price: {s.price or 'Contact for price'}." for s in clinic.services])
        prompt += f"""

Here is a list of services offered by the clinic:
{service_list}
"""

    # Add context from the vector database (RAG) if any was found
    if rag_context:
        prompt += f"""

Here is some additional information from the clinic's documents that might be relevant to the user's question. Use this information to provide a more accurate and detailed response. If the user's question is answered here, prioritize this information.
---
{rag_context}
---
"""

    prompt += "\nNow, please respond to the user's message."
    
    return prompt