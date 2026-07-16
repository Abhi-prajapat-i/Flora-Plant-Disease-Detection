from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
load_dotenv()
llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
      )

if __name__ == "__main__":
    pass
    # response = llm.invoke("How is the PM of INDIA.")
    # print(response.content)

    prompt = ChatPromptTemplate.from_template(
        """
            you are a healful AI assistant.

            Answer the following question in one line.

            Question : {question}
        """
    )

    chain = prompt | llm

    response = chain.invoke(
    {
        "question": "Who is the Prime Minister of India in 2026?"
    }
    )

    print(response.content)
