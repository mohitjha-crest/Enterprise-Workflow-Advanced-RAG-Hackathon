from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import requests
import os
from sentence_transformers.cross_encoder import CrossEncoder

from platforms.vectara_platform.vectara import request_vectara_sop, request_vectara_sop_and_chat_history

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
def get_output(context, query):

    url = "https://api.together.xyz/v1/chat/completions"

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {
                "role": 'system',
                "content": f'{summary_template}'
            },
            {
                "role": 'user',
                "content": f'Question: {query} Information: {context}'
            }
        ],
        "stop": ["</s>"],
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": os.environ.get("TOGETHER_API_TOKEN")

    }

    response = requests.post(url, json=payload, headers=headers)
    response = response.json().get("choices")
    choices = response[0]
    mistral_output = choices.get("message", {}).get("content")
    print(f"{mistral_output=}")
    mistral_score = find_hhem_score(mistral_output, context)
    if mistral_score < 0.7:
        gpt_output = get_gpt_op(context, query)
        gpt_score = find_hhem_score(gpt_output, context)
        if gpt_score > mistral_score:
            return gpt_output
        else:
            return mistral_output
    else:
        return mistral_output

def get_gpt_op(context, query):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",
                     openai_api_key=OPENAI_API_KEY)

    summary_prompt_template = PromptTemplate(
        input_variables=["context", "query"],
        template=summary_template,
    )

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    gpt_answer = chain.invoke(
        input={"context": context, "query": query}).get("text")
    print(f"{gpt_answer=}")
    return gpt_answer

def find_hhem_score(answer: str, statement: str
                    ) -> float:

    model = CrossEncoder("vectara/hallucination_evaluation_model")

    list_statement = [statement]
    ranks = model.rank(answer, list_statement)
    rank = [rank["score"] for rank in ranks]
    return float(rank[0])

def request_crag_sop(query):
    output_result = request_vectara_sop(query)
    context_ = output_result['responseSet'][0]['response'][0]['text']
    output_result = get_output(context=context_, query=query)
    return output_result

def request_crag_sop_and_chat_history(query):
    output_result = request_vectara_sop_and_chat_history(query)
    context_ = output_result['responseSet'][0]['response'][0]['text']
    output_result = get_output(context=context_, query=query)
    return output_result
