from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
summary_template = """As Crest Data Systems' assistant, provide precise, complete answers and engage smoothly.
            Note that you should answer user queries based on the documents you have indexed. Ensure to give your answer in well-defined steps.
            Ensure to answer all the questions with respect to crest data systems.
            If users ask you about disabling some security related applications, based on your ethical and compliance boundaries, ask them to contact IT team for further assistance.
            If you don't know the correct answer, prepend the following at the start of the response: Although I couldn't find anything in our knowledge base, here are the general steps to follow. and append the following at the end of the answer: \"Please contact Crest IT support at IT Helpdesk google chat for further assistance.\"

    Context: {context}
    Query: {query}
    Answer: 
    """
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",
                 openai_api_key=OPENAI_API_KEY)
# Creating a prompt template for the summary
summary_prompt_template = PromptTemplate(
    input_variables=["context", "query"],
    template=summary_template,
)

# Creating an LLMChain object with the ChatOpenAI model and the summary prompt template
chain = LLMChain(llm=llm, prompt=summary_prompt_template)


def get_output(context, query):
    gpt_answer = chain.invoke(
        input={"context": context, "query": query}).get("text")
    return gpt_answer
