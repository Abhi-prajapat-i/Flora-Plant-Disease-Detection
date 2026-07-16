MAX_HISTORY_MESSAGES = 10
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def get_prompt(crop, language, disease):
    prompt = f"""
        You are an agricultural expert.

        Plant: {crop}
        Prediction: {disease}
        Language: {language}

        The prediction is already confirmed. Do NOT change it or diagnose another disease.

        If the prediction is "Healthy":
        - State that the plant is healthy.
        - Provide only:
        - Plant Care (watering, fertilizer, sunlight, soil)
        - Prevention Tips
        - Good farming practices
        - Do NOT mention symptoms, causes, disease severity, treatments, recovery, or infected leaves.

        Otherwise, provide:
        - Description
        - Symptoms
        - Causes
        - Chemical Treatment
        - Organic Treatment
        - Prevention
        - Plant Care
        - Severity (Low/Medium/High)
        - Remove infected parts? (Yes/No + reason)
        - Expected Recovery
        - When to consult an agricultural expert

        Rules:
        - Follow the prediction exactly.
        - Never invent or assume another disease.
        - Reply only in {language}.
        - English: simple English.
        - Hindi: simple Hindi.
        - Hinglish: Hindi written in English letters.
        - Use clear headings and bullet points.
        - Recommend only safe, commonly accepted practices and remind users to follow product labels and local agricultural guidelines.
        """
    return prompt


def build_chat_messages(crop, disease, treatment_advice, history, question):
    """
    Build a LangChain message list that gives the LLM:
    1) A system message anchoring it to the diagnosed crop/disease and the
       treatment advice already given (so it never forgets the recommendation).
    2) The last MAX_HISTORY_MESSAGES turns of the conversation (short-term memory).
    3) The new user question.
    """

    system_content = (
        f"You are Flora, an AI plant treatment advisor.\n"
        f"Crop: {crop}\n"
        f"Diagnosed Disease: {disease}\n"
        f"Treatment advice already given to the user:\n{treatment_advice or 'Not generated yet.'}\n\n"
        "Always stay consistent with this diagnosis and the treatment advice above. "
        f"Answer in one line."
    )

    messages = [SystemMessage(content=system_content)]

    # Keep only the last MAX_HISTORY_MESSAGES messages for short-term memory
    recent_history = history[-MAX_HISTORY_MESSAGES:]

    for msg in recent_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=question))

    return messages